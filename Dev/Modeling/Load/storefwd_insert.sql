INSERT INTO nyctaxidata.dim_store_and_fwd (flag_id, store_and_fwd_flag, description)
SELECT DISTINCT
  Store_and_fwd_flag,
  CASE Store_and_fwd_flag
    WHEN 'Y' THEN 'Yes'
    WHEN 'N' THEN 'No'
    ELSE 'Unknown'
  END AS store_and_fwd_flag,
  CASE Store_and_fwd_flag
    WHEN 'Y' THEN 'Trip record was stored and forwarded'
    WHEN 'N' THEN 'Trip record was sent in real-time'
    ELSE 'Unknown status'
  END AS description
FROM `nyctaxidata.taxialyx`;
