-- #standardSQL
select *
from `bigquery-public-data.crypto_ethereum.balances`
order by eth_balance desc
limit 10