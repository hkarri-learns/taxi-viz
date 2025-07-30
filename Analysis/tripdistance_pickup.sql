#Trip distance varying by pickup location

Select 
lo.zone as pickup_zone, lo.location_id as pickup_location_id, ROUND(AVG(trip_distance),2) as Average_trip_distance 
FROM `nyctaxidata.FACT_TAXI_TRIP` ny
JOIN `nyctaxidata.dim_location` lo ON ny.pickup_location_id = lo.location_id
GROUP BY lo.location_id, pickup_zone
ORDER BY Average_trip_distance DESC