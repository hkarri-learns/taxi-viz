
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, when, to_timestamp, lit, unix_timestamp, round,
    current_timestamp, year as get_year, month as get_month,
    percentile_approx, count, expr
)
from pyspark.sql.types import IntegerType, DoubleType
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Start Spark session
spark = SparkSession.builder \
    .appName("NYC Yellow Taxi Data Cleaning - Silver Layer") \
    .getOrCreate()

# Set dynamic partition overwrite mode
spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")

def transform_data(year, month):
    try:
        # Define paths
        input_path = f"gs://nyc_taxidata/yellow_taxi_data_bronze/{year}/{month:02d}/yellow_tripdata_{year}-{month:02d}.parquet"
        silver_output_path = "gs://nyc_taxidata/yellow_taxi_data_silver"
        cleaned_output_path = "gs://nyc_taxidata/yellow_taxi_data_silver_cleaned"
        summary_output_path = f"gs://nyc_taxidata/yellow_taxi_data_summary/yellow_tripdata_{year}-{month:02d}.csv"

        logger.info(f"Reading data from: {input_path}")
        df_raw = spark.read.parquet(input_path)

        # Standardize types
        df = df_raw.withColumn("tpep_pickup_datetime", to_timestamp("tpep_pickup_datetime"))\
                             .withColumn("tpep_dropoff_datetime", to_timestamp("tpep_dropoff_datetime"))\
                             .withColumn("VendorID", col("VendorID").cast(IntegerType()))\
                             .withColumn("passenger_count", col("passenger_count").cast(IntegerType()))\
                             .withColumn("trip_distance", col("trip_distance").cast(DoubleType()))\
                             .withColumn("RatecodeID", col("RatecodeID").cast(IntegerType()))\
                             .withColumn("payment_type", col("payment_type").cast(IntegerType()))

        # Categorical filters
        valid_vendor_ids = [1, 2, 6, 7]
        valid_ratecode_ids = [1, 2, 3, 4, 5, 6, 99]
        valid_payment_types = [0, 1, 2, 3, 4, 5, 6]

        df = df.filter(col("VendorID").isin(valid_vendor_ids))\
                 .filter(col("RatecodeID").isin(valid_ratecode_ids))\
                 .filter(col("payment_type").isin(valid_payment_types))\
                 .filter(col("store_and_fwd_flag").isin("Y", "N"))

        # Numeric filters
        df = df.filter((col("trip_distance") > 0) &
                       (col("fare_amount") >= 0) &
                       (col("total_amount") >= 0) &
                       (col("passenger_count") > 0) &
                       (col("passenger_count") <= 6))

        # Temporal validation
        now = current_timestamp()
        df = df.filter((col("tpep_pickup_datetime") < col("tpep_dropoff_datetime")) &
                       (col("tpep_pickup_datetime") <= now))

        # Derive trip duration and speed
        df = df.withColumn("trip_duration_minutes",
                           (unix_timestamp("tpep_dropoff_datetime") - unix_timestamp("tpep_pickup_datetime")) / 60)

        df = df.withColumn("average_speed_mph",
                           when(col("trip_duration_minutes") > 0,
                                round(col("trip_distance") / (col("trip_duration_minutes") / 60), 2))
                           .otherwise(None))

        # Add partition columns
        df = df.withColumn("year", lit(int(year))).withColumn("month", lit(int(month)))

        # Write full dataset
        df.write.mode("overwrite").partitionBy("year", "month").parquet(silver_output_path)

        # Compute IQR for outlier detection
        fields = ["trip_distance", "total_amount", "tip_amount"]
        thresholds = {}

        for field in fields:
            q1, q3 = df.select(
                percentile_approx(field, 0.25).alias("q1"),
                percentile_approx(field, 0.75).alias("q3")
            ).first()
            iqr = q3 - q1
            thresholds[field] = (q1 - 1.5 * iqr, q3 + 1.5 * iqr)

        for field in fields:
            lb, ub = thresholds[field]
            df = df.withColumn(f"{field}_is_outlier", (col(field) < lb) | (col(field) > ub))

        # Filter cleaned dataset
        df_cleaned = df.filter(
            (col("trip_distance_is_outlier") == False) &
            (col("total_amount_is_outlier") == False) &
            (col("tip_amount_is_outlier") == False)
        )

        # Write cleaned dataset
        df_cleaned.write.mode("overwrite").partitionBy("year", "month").parquet(cleaned_output_path)

        # Summary stats
        record_count = df.count()
        cleaned_count = df_cleaned.count()
        outlier_summary = spark.createDataFrame([{
            "year": year,
            "month": month,
            "record_count": record_count,
            "cleaned_record_count": cleaned_count,
            "trip_distance_outlier_pct": df.filter(col("trip_distance_is_outlier")).count() / record_count * 100,
            "total_amount_outlier_pct": df.filter(col("total_amount_is_outlier")).count() / record_count * 100,
            "tip_amount_outlier_pct": df.filter(col("tip_amount_is_outlier")).count() / record_count * 100
        }])

        # Write summary as CSV
        outlier_summary.coalesce(1).write.mode("overwrite").option("header", "true").csv(summary_output_path)

        logger.info(f"Completed processing and summary for {year}-{month:02d}")

    except Exception as e:
        logger.error(f"Failed processing for {year}-{month:02d}: {str(e)}")

def main():
    years = ['2021', '2022', '2023', '2024']
    for year in years:
        for month in range(1, 13):
            transform_data(year, month)

    logger.info("Data transformation completed for all months.")

if __name__ == "__main__":
    main()
    spark.stop()
