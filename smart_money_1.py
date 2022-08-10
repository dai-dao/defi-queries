# Altair viz doc: https://altair-viz.github.io/user_guide/customization.html#adjusting-axis-labels
# Streamlit altair doc: https://docs.streamlit.io/library/api-reference/charts/st.altair_chart

import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery
import pandas as pd
import altair as alt


# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)


# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 1000 min.
@st.experimental_memo(ttl=60000)
def run_query(query):
    df = pd.read_gbq(query, credentials=credentials)
    return df



transaction_counts_by_date = run_query("""
    SELECT COUNT(*) AS transac_count, DATE(ad.block_timestamp) AS transact_date 
    FROM `alpine-effort-357120.top_eth_trades.address_1` ad
    GROUP BY transact_date
    ORDER BY transact_date
""")
transaction_counts_by_date['transact_date'] = pd.to_datetime(transaction_counts_by_date['transact_date'])



transaction_counts_by_weekday = run_query("""
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
ORDER BY day_of_week
""")



transaction_counts_by_hour = run_query("""
SELECT COUNT(*) AS transac_count, 
        EXTRACT(HOUR FROM ad.block_timestamp) AS hour_of_day,
    FROM `alpine-effort-357120.top_eth_trades.address_1` ad
GROUP BY hour_of_day
ORDER BY hour_of_day
""")




def get_chart(title, data, x, y, x_title):

    chart = alt.Chart(data, title=title)\
                .mark_bar()\
                .encode(x=alt.X(x, axis=alt.Axis(title=None)),
                        y=alt.X(y, axis=alt.Axis(title="Transactions")))
    chart.configure_axisX(title=None)
    lines = (chart)


    # Draw points on the line, and highlight based on selection
    hover = alt.selection_single(
                    fields=[x],
                    nearest=True,
                    on="mouseover",
                    empty="none",
        )
    points = lines.transform_filter(hover).mark_circle(size=65)

    # Draw a rule at the location of the selection
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x=x,
            y=y,
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip(x, title=x_title),
                alt.Tooltip(y, title="Transaction Counts"),
            ],
        )
        .add_selection(hover)
    )
    return (lines + points + tooltips).interactive()






transaction_counts_by_date_chart = get_chart("Activity", transaction_counts_by_date, 
                                            "transact_date", "transac_count", "Date")
transaction_counts_by_weekday_chart = get_chart("Day of week", transaction_counts_by_weekday, 
                                            "day_of_week", "transac_count", "")
transaction_counts_by_hour_chart = get_chart("Hour of day (UTC)", transaction_counts_by_hour, 
                                            "hour_of_day", "transac_count", "")



st.altair_chart(
    transaction_counts_by_date_chart.interactive(),
    use_container_width=True
)


st.altair_chart(
    transaction_counts_by_weekday_chart.interactive(),
    use_container_width=False
)


st.altair_chart(
    transaction_counts_by_hour_chart.interactive(),
    use_container_width=False
)