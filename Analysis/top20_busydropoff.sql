SELECT lo.location_id, COUNT(*) as trip_count FROM `nyctaxidata.FACT_TAXI_TRIP` ft
JOIN `nyctaxidata.dim_location` lo
ON lo.location_id = ft.dropoff_location_id
GROUP BY location_id
ORDER BY trip_count DESC
LIMIT 20
