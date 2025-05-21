CREATE TABLE nyc_taxidata.taxi_data_fact(
  trip_id STRING,
  vendor_id INT64,
  tpep_pickup_datetime TIMESTAMP,
  tpep_dropoff_datetime TIMESTAMP,
  passenger_count INT64,
  trip_distance FLOAT64,
  ratecode_id INT64,
  store_and_fwd_flag STRING,
  pickup_location_id INT64,
  dropoff_location_id INT64,
  payment_type INT64,
  fare_amount FLOAT64,
  extra FLOAT64,
  mta_tax FLOAT64,
  tip_amount FLOAT64,
  tolls_amount FLOAT64,
  improvement_surcharge FLOAT64,
  total_amount FLOAT64,
  congestion_surcharge FLOAT64,
  airport_fee FLOAT64,
  trip_duration_minutes FLOAT64,
  average_speed_mph FLOAT64
);

INSERT INTO nyc_taxidata.taxi_data_fact
SELECT
  GENERATE_UUID() AS trip_id,
  s.vendorid,
  s.tpep_pickup_datetime,
  s.tpep_dropoff_datetime,
  s.passenger_count,
  s.trip_distance,
  s.ratecodeid,
  s.store_and_fwd_flag,
  pl.location_id AS pickup_location_id,
  dl.location_id AS dropoff_location_id,
  s.payment_type,
  s.fare_amount,
  s.extra,
  s.mta_tax,
  s.tip_amount,
  s.tolls_amount,
  s.improvement_surcharge,
  s.total_amount,
  s.congestion_surcharge,
  s.airport_fee,
  s.trip_duration_minutes,
  s.average_speed_mph
FROM nyc_taxidata.schema_table s
JOIN nyc_taxidata.location_dime pl ON s.PULocationID = pl.location_id
JOIN nyc_taxidata.location_dime dl ON s.DOLocationID = dl.location_id
