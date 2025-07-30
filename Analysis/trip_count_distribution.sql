#Distribution of passenger count
SELECT passenger_count,
COUNT(*) as trip_count,
ROUND(COUNT(*)*100/ SUM(COUNT(*)) OVER (), 2) as percentage
FROM `nyctaxidata.FACT_TAXI_TRIP`
GROUP BY passenger_count
ORDER BY passenger_count