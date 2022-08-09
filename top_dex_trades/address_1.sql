-- Process entire table
-- select *
-- from `bigquery-public-data.crypto_ethereum.transactions`
-- where from_address = '0x0f4ee9631f4be0a63756515141281a3e2b293bbe'
-- OR to_address = '0x0f4ee9631f4be0a63756515141281a3e2b293bbe'


SELECT COUNT(*) AS transac_count, DATE(ad.block_timestamp) AS transact_date 
FROM `alpine-effort-357120.top_eth_trades.address_1` ad
GROUP BY transact_date
ORDER BY transact_date;




SELECT a.transac_count, 
        CASE
            WHEN a.day_of_week = 0 THEN 7
            ELSE a.day_of_week
        END AS day_of_week
FROM (
    SELECT COUNT(*) AS transac_count, 
        EXTRACT(DAYOFWEEK FROM ad.block_timestamp)-1 AS day_of_week,
    FROM `alpine-effort-357120.top_eth_trades.address_1` ad
    GROUP BY day_of_week
    ORDER BY day_of_week
) a
ORDER BY day_of_week;





SELECT COUNT(*) AS transac_count, 
        EXTRACT(HOUR FROM ad.block_timestamp) AS hour_of_day,
    FROM `alpine-effort-357120.top_eth_trades.address_1` ad
GROUP BY hour_of_day
ORDER BY hour_of_day;

