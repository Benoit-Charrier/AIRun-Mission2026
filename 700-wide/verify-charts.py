# K 7.W.6 — Inline chart verification (notebook equivalent)
# Confirms charts show real data from gold tables before Streamlit deploy

import duckdb
import pandas as pd
import plotly.express as px
import plotly.io as pio
import os

# Load gold tables
sales = pd.read_parquet('gold/daily_sales_by_category.parquet')
returns = pd.read_parquet('gold/returns_rate.parquet')
sales['order_date'] = pd.to_datetime(sales['order_date'])
returns['order_date'] = pd.to_datetime(returns['order_date'])

# ---- Verification assertions ----
# Chart 1: all 4 regions present, bars vary
regions = set(sales['region'].unique())
assert regions == {'North', 'South', 'East', 'West'}, f"Missing regions: {regions}"
rev_by_region = sales.groupby('region')['total_revenue'].sum()
assert rev_by_region.std() > 0, "Revenue bars are flat (no variation)"
print(f"Chart 1 OK — {len(regions)} regions, revenue range: "
      f"${rev_by_region.min():.0f}..${rev_by_region.max():.0f}")

# Chart 2: line varies (not flat at 0)
assert returns['returns_rate_pct'].std() > 0, "Returns rate is flat (no variation)"
rr_min = returns['returns_rate_pct'].min()
rr_max = returns['returns_rate_pct'].max()
print(f"Chart 2 OK — returns rate range: {rr_min:.1f}%..{rr_max:.1f}%")

# Metric cards
total_rev = sales['total_revenue'].sum()
avg_rr = returns['returns_rate_pct'].mean()
print(f"Metric cards — Total Revenue: ${total_rev:,.0f} | Avg Returns Rate: {avg_rr:.1f}%")

# Data last updated
last_date = sales['order_date'].max().date()
print(f"Data last updated: {last_date}")

# ---- Generate chart images for artefact ----
os.makedirs('kata-workspace', exist_ok=True)

# Build inline charts
rev_agg = sales.groupby(['region', 'product_category'], as_index=False)['total_revenue'].sum()
fig1 = px.bar(rev_agg, x='region', y='total_revenue',
              color='product_category', barmode='group',
              title='Total Revenue by Region & Category',
              labels={'total_revenue': 'Revenue ($)', 'region': 'Region'})

fig2 = px.line(returns, x='order_date', y='returns_rate_pct',
               title='Returns Rate Over Time (%)',
               labels={'returns_rate_pct': 'Returns Rate (%)', 'order_date': 'Date'})
fig2.add_hline(y=avg_rr, line_dash='dot',
               annotation_text='Average', line_color='grey')

# Save as HTML (inline chart record — no kaleido required)
fig1.write_html('kata-workspace/chart1-revenue-by-region.html')
fig2.write_html('kata-workspace/chart2-returns-rate.html')
print("chart1-revenue-by-region.html and chart2-returns-rate.html written to kata-workspace/")
print("\nVerification PASSED — charts show real data from gold tables")
print("Note: one improvement — add a 'pending orders excluded' annotation to Chart 2")
