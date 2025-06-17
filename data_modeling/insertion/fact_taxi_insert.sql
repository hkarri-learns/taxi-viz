INSERT INTO `nyctaxidata.FACT_TAXI_TRIP`(
  trip_id,
  vendor_id,
  rate_code_id,
  pickup_location_id,
  dropoff_location_id,
  datetime_id,
  payment_type_id,
  store_and_fwd_flag,
  passenger_count,
  trip_distance,
  fare_amount,
  extra,
  mta_tax,
  improvement_surcharge,
  tip_amount,
  tolls_amount,
  total_amount,
  trip_duration_minutes
)

SELECT
  GENERATE_UUID() AS trip_id,
  VendorID,
  RateCodeID,
  PULocationID AS pickup_location_id,
  DOLocationID AS dropoff_location_id,
  FORMAT_TIMESTAMP('%Y%m%d%H%M%S', tpep_pickup_datetime) AS datetime_id,
  Payment_type AS payment_type_id,
  Store_and_fwd_flag,
  Passenger_count,
  Trip_distance,
  Fare_amount,
  Extra,
  MTA_tax,
  Improvement_surcharge,
  Tip_amount,
  Tolls_amount,
  Total_amount,
  TIMESTAMP_DIFF(tpep_dropoff_datetime, tpep_pickup_datetime, MINUTE) AS trip_duration_minutes
FROM `nyctaxidata.taxialyx`
WHERE tpep_pickup_datetime IS NOT NULL AND tpep_dropoff_datetime IS NOT NULL;