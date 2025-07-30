CREATE OR REPLACE TABLE nyctaxidata.dim_datetime (
  datetime_id STRING,
  pickup_datetime DATETIME,
  dropoff_datetime DATETIME,
  pickup_hour INT64,
  pickup_day INT64,
  pickup_month INT64,
  pickup_year INT64,
  pickup_weekday STRING
);
