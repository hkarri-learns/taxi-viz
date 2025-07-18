-- Busiest hour in fact_taxi_trip data
SELECT
  dim_datetime.pickup_hour,
  COUNT(*) AS total_trips
FROM
  `argon-tractor-456103-i7`.`nyctaxidata`.`FACT_TAXI_TRIP` AS FACT_TAXI_TRIP
LEFT OUTER JOIN
  `argon-tractor-456103-i7`.`nyctaxidata`.`dim_datetime` AS dim_datetime
ON
  FACT_TAXI_TRIP.datetime_id = dim_datetime.datetime_id
GROUP BY
  1
ORDER BY
  2 DESC
LIMIT
  1;