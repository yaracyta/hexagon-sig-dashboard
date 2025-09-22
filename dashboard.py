import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="AdventureWorks Sales Dashboard", layout="wide")

# Title
st.title("AdventureWorks Sales Dashboard 🚀")
st.write("Interactive dashboard to explore sales performance by date, product, and region.")

# Load data
df = pd.read_excel("query.xlsx")
df["OrderDate"] = pd.to_datetime(df["OrderDate"], errors="coerce")
df = df.dropna(subset=["OrderDate"])
df["Year"] = df["OrderDate"].dt.year
df["Month"] = df["OrderDate"].dt.month
df["YearMonth"] = df["OrderDate"].dt.to_period("M").astype(str)

# Sidebar filters
st.sidebar.header("Filters")
dmin, dmax = df["OrderDate"].min().date(), df["OrderDate"].max().date()
date_range = st.sidebar.date_input("Date range", (dmin, dmax))
prod_opts = sorted(df["ProductName"].unique().tolist())
reg_opts = sorted(df["Region"].unique().tolist())
prod_sel = st.sidebar.multiselect("Products", prod_opts, default=prod_opts)
reg_sel = st.sidebar.multiselect("Regions", reg_opts, default=reg_opts)

# Apply filters
if len(date_range) == 2:
    df_f = df[
        (df["OrderDate"].dt.date >= date_range[0]) &
        (df["OrderDate"].dt.date <= date_range[1]) &
        (df["ProductName"].isin(prod_sel)) &
        (df["Region"].isin(reg_sel))
    ]
elif len(date_range) == 1:
    df_f = df[
        (df["OrderDate"].dt.date == date_range[0]) &
        (df["ProductName"].isin(prod_sel)) &
        (df["Region"].isin(reg_sel))
    ]
else:
    df_f = df[
        (df["ProductName"].isin(prod_sel)) &
        (df["Region"].isin(reg_sel))
    ]

# KPI
kpi = df_f["TotalDue"].sum()
st.metric("💰 Total Sales (filtered)", f"{kpi:,.2f}")

# Layout columns
col1, col2 = st.columns(2)

# Bar chart - Top products
with col1:
    st.subheader("Top 10 Products by Sales")
    top_prod = (
        df_f.groupby("ProductName", as_index=False)["TotalDue"].sum()
        .sort_values("TotalDue", ascending=False)
        .head(10)
    )
    fig1 = px.bar(
        top_prod,
        x="ProductName",
        y="TotalDue",
        title="Top 10 Products by Sales",
        labels={"ProductName": "Product", "TotalDue": "Total Sales"},
        text_auto=".2s"
    )
    fig1.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig1, use_container_width=True)


# Line chart - Sales over time
with col2:
    st.subheader("Sales Over Time (Year-Month)")
    sales_ts = (
        df_f.groupby("YearMonth", as_index=False)["TotalDue"].sum()
        .sort_values("YearMonth")
    )
    fig2 = px.line(
        sales_ts,
        x="YearMonth",
        y="TotalDue",
        markers=True,
        title="Sales Over Time (Year-Month)",
        labels={"YearMonth": "Period", "TotalDue": "Total Sales"}
    )
    fig2.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig2, use_container_width=True)


