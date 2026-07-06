# K 7.W.6 — Streamlit dashboard — Nordstar Sales Performance
# Run: streamlit run app.py (from kata-workspace/ with gold/ sibling folder)
# Inline equivalent: replace st.plotly_chart(fig) with fig.show()

import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Sales Performance Dashboard", layout="wide")
st.title("Sales Performance Dashboard")
st.caption("Nordstar Customer 360 — Retail Transactions (Synthetic)")

# --- Load gold tables ---
base = os.path.join(os.path.dirname(__file__), '..', 'gold')
sales = pd.read_parquet(os.path.join(base, 'daily_sales_by_category.parquet'))
returns = pd.read_parquet(os.path.join(base, 'returns_rate.parquet'))

sales['order_date'] = pd.to_datetime(sales['order_date'])
returns['order_date'] = pd.to_datetime(returns['order_date'])

# --- Sidebar date filter ---
max_date = sales['order_date'].max()
min_date = max_date - pd.Timedelta(days=30)
date_range = st.sidebar.date_input(
    "Date range",
    value=(min_date.date(), max_date.date()),
    min_value=sales['order_date'].min().date(),
    max_value=max_date.date(),
)
if len(date_range) == 2:
    start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
    sales_f = sales[(sales['order_date'] >= start) & (sales['order_date'] <= end)]
    returns_f = returns[(returns['order_date'] >= start) & (returns['order_date'] <= end)]
else:
    sales_f = sales
    returns_f = returns

# --- Metric cards ---
col1, col2 = st.columns(2)
col1.metric("Total Revenue", f"${sales_f['total_revenue'].sum():,.0f}")
col2.metric("Avg Returns Rate", f"{returns_f['returns_rate_pct'].mean():.1f}%")

# --- Chart 1: Revenue by region, coloured by category ---
rev_agg = sales_f.groupby(['region', 'product_category'], as_index=False)['total_revenue'].sum()
fig1 = px.bar(rev_agg, x='region', y='total_revenue',
              color='product_category', barmode='group',
              title='Total Revenue by Region & Category',
              labels={'total_revenue': 'Revenue ($)', 'region': 'Region'})
st.plotly_chart(fig1, use_container_width=True)

# --- Chart 2: Returns rate over time ---
fig2 = px.line(returns_f, x='order_date', y='returns_rate_pct',
               title='Returns Rate Over Time (%)',
               labels={'returns_rate_pct': 'Returns Rate (%)', 'order_date': 'Date'})
fig2.add_hline(y=returns_f['returns_rate_pct'].mean(), line_dash='dot',
               annotation_text='Average', line_color='grey')
st.plotly_chart(fig2, use_container_width=True)

# --- Footer ---
st.caption(f"Data last updated: {sales['order_date'].max().date()}")
