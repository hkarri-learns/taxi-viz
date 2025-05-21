SELECT trip_id FROM nyc_taxidata.taxi_data_fact 
Where pickup_location_id IS NULL OR
dropoff_location_id IS NULL OR
fare_amount is NULL OR
trip_distance is null


