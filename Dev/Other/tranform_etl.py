from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, when, to_timestamp, lit, unix_timestamp, round,
    current_timestamp, year as get_year, month as get_month
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
        output_path = "gs://nyc_taxidata/yellow_taxi_data_silver"

        logger.info(f"Reading data from: {input_path}")
        df_raw = spark.read.parquet(input_path)

        # Standardize data types
        df = df_raw.withColumn("tpep_pickup_datetime", to_timestamp("tpep_pickup_datetime")) \
            .withColumn("tpep_dropoff_datetime", to_timestamp("tpep_dropoff_datetime")) \
            .withColumn("VendorID", col("VendorID").cast(IntegerType())) \
            .withColumn("passenger_count", col("passenger_count").cast(IntegerType())) \
            .withColumn("trip_distance", col("trip_distance").cast(DoubleType())) \
            .withColumn("RatecodeID", col("RatecodeID").cast(IntegerType())) \
            .withColumn("payment_type", col("payment_type").cast(IntegerType()))

        # Filter valid categorical values
        valid_vendor_ids = [1, 2, 6, 7]
        valid_ratecode_ids = [1, 2, 3, 4, 5, 6, 99]
        valid_payment_types = [0, 1, 2, 3, 4, 5, 6]

        df = df.filter(col("VendorID").isin(valid_vendor_ids)) \
            .filter(col("RatecodeID").isin(valid_ratecode_ids)) \
            .filter(col("payment_type").isin(valid_payment_types)) \
            .filter(col("store_and_fwd_flag").isin("Y", "N"))

        # Handle anomalous numeric values
        df = df.filter((col("trip_distance") > 0) &
                       (col("fare_amount") >= 0) &
                       (col("total_amount") >= 0) &
                       (col("passenger_count") > 0) &
                       (col("passenger_count") <= 6))

        # Temporal validation
        now = current_timestamp()
        df = df.filter((col("tpep_pickup_datetime") < col("tpep_dropoff_datetime")) &
                       (col("tpep_pickup_datetime") <= now))

        # Derive trip duration and average speed
        df = df.withColumn("trip_duration_minutes",
                           (unix_timestamp("tpep_dropoff_datetime") - unix_timestamp("tpep_pickup_datetime")) / 60)

        df = df.withColumn("average_speed_mph",
                           when(col("trip_duration_minutes") > 0,
                                round(col("trip_distance") / (col("trip_duration_minutes") / 60), 2))
                           .otherwise(None))

        # Add partition columns
        df = df.withColumn("year", lit(int(year))).withColumn("month", lit(int(month)))

        # Write to Silver Layer
        df.write.mode("overwrite") \
            .partitionBy("year", "month") \
            .parquet(output_path)

        logger.info(f"Transformed data written to Silver Layer for {year}-{month:02d}")

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
