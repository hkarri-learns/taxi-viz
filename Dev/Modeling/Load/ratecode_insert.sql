INSERT INTO `nyctaxidata.dim_rate_code` (rate_code_id, rate_description)
SELECT DISTINCT
  RatecodeID,
  CASE RatecodeID
    WHEN 1 THEN 'Standard rate'
    WHEN 2 THEN 'JFK'
    WHEN 3 THEN 'Newark'
    WHEN 4 THEN 'Nassau or Westchester'
    WHEN 5 THEN 'Negotiated fare'
    WHEN 6 THEN 'Group ride'
    ELSE 'Unknown'
  END AS rate_description
FROM `nyctaxidata.taxialyx`;
