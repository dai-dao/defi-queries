-- nice dashboard
-- https://datastudio.google.com/u/0/reporting/197An_pAkoJ_fAKCRTY6GO608j2mwz8CO/page/yJtg

with daily_transactions as (
    select date(block_timestamp) as date, count(*) as count
    from `bigquery-public-data.crypto_bitcoin.transactions`
    group by date
)
select date_trunc(date, WEEK) as week, cast(avg(count) as INT64) as count
from daily_transactions
group by week
order by week