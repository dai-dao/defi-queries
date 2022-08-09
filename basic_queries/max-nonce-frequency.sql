SELECT
	max_nonce,
	COUNT(max_nonce) AS num_addresses
FROM
(
	SELECT 
      MAX(nonce) AS max_nonce,
      from_address
	FROM `bigquery-public-data.crypto_ethereum.transactions` AS txns
	GROUP BY from_address
)
GROUP BY max_nonce
ORDER BY max_nonce ASC