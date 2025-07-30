SELECT dt.pickup_weekday WeekDay,
ROUND(AVG(trip_duration_minutes)) Average_Trip_Minutes, 
ROUND(AVG(trip_distance)) Trip_Distance  
FROM `nyctaxidata.FACT_TAXI_TRIP` nc
JOIN `nyctaxidata.dim_datetime` dt ON nc.datetime_id = dt.datetime_id
GROUP BY dt.pickup_weekday
ORDER BY Trip_Distance, Average_Trip_Minutes
