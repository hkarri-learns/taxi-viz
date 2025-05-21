CREATE TABLE nyc_taxidata.location_dime(
  location_id INT64,
  borough STRING,
  zone STRING,
  service_zone STRING
);

INSERT INTO nyc_taxidata.location_dime (location_id, borough, zone, service_zone)
SELECT
  CAST(LocationID as INT64),
  Borough,
  Zone,
  service_zone
FROM nyc_taxidata.lookup_staging
