INSERT INTO nyctaxidata.dim_payment_type (payment_type_id, payment_method)
SELECT DISTINCT
  Payment_type,
  CASE Payment_type
    WHEN 0 THEN 'Flex Fare trip'
    WHEN 1 THEN 'Credit card'
    WHEN 2 THEN 'Cash'
    WHEN 3 THEN 'No charge'
    WHEN 4 THEN 'Dispute'
    WHEN 5 THEN 'Unknown'
    WHEN 6 THEN 'Voided trip'
    ELSE 'Other'
  END AS payment_method
FROM `nyctaxidata.taxialyx`;