INSERT INTO nyctaxidata.dim_location (location_id, borough, zone, service_zone)
SELECT DISTINCT
  LocationID AS location_id,
  Borough,
  Zone,
  service_zone
FROM `nyctaxidata.lookup`;