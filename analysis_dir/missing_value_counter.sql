SELECT COUNT(*) as missing_value_count
FROM nyc_taxidata.taxi_data_fact
WHERE pickup_location_id is NULL OR
dropoff_location_id is NULL OR
fare_amount is NULL OR
trip_distance is NULL