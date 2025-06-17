INSERT INTO nyctaxidata.dim_datetime (
  datetime_id, pickup_datetime, dropoff_datetime,
  pickup_hour, pickup_day, pickup_month,
  pickup_year, pickup_weekday
)
SELECT DISTINCT
  FORMAT_TIMESTAMP('%Y%m%d%H%M%S', tpep_pickup_datetime) AS datetime_id,
  DATETIME(tpep_pickup_datetime) as pickup_datetime,
  DATETIME(tpep_dropoff_datetime) as dropoff_datetime,
  EXTRACT(HOUR FROM tpep_pickup_datetime),
  EXTRACT(DAY FROM tpep_pickup_datetime),
  EXTRACT(MONTH FROM tpep_pickup_datetime),
  EXTRACT(YEAR FROM tpep_pickup_datetime),
  FORMAT_TIMESTAMP('%A', tpep_pickup_datetime)
FROM `nyctaxidata.taxialyx`;