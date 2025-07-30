INSERT INTO `nyctaxidata.dim_vendor`(vendor_id, vendor_name)
SELECT DISTINCT
  VendorID,
  CASE VendorID
    WHEN 1 THEN 'Creative Mobile Technologies, LLC'
    WHEN 2 THEN 'Curb Mobility, LLC'
    WHEN 6 THEN 'Myle Technologies Inc'
    WHEN 7 THEN 'Helix'
    ELSE 'Unknown'
  END AS vendor_name
FROM `nyctaxidata.taxialyx`
