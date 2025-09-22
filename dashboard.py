import streamlit as st

st.title("Meu Primeiro Dashboard 🚀")
st.write("Se você está vendo isso no navegador, o Streamlit está funcionando!")

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Vendas", layout="wide")

df = pd.read_excel("query.xlsx")
df["OrderDate"] = pd.to_datetime(df["OrderDate"], errors="coerce")
df = df.dropna(subset=["OrderDate"])
df["Year"] = df["OrderDate"].dt.year
df["Month"] = df["OrderDate"].dt.month
df["YearMonth"] = df["OrderDate"].dt.to_period("M").astype(str)

st.sidebar.header("Filtros")
dmin, dmax = df["OrderDate"].min().date(), df["OrderDate"].max().date()
date_range = st.sidebar.date_input("Intervalo de datas", (dmin, dmax))
prod_opts = sorted(df["ProductName"].unique().tolist())
reg_opts = sorted(df["Region"].unique().tolist())
prod_sel = st.sidebar.multiselect("Produtos", prod_opts, default=prod_opts)
reg_sel = st.sidebar.multiselect("Regiões", reg_opts, default=reg_opts)

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

kpi = df_f["TotalDue"].sum()
st.metric("💰 Total de Vendas (filtrado)", f"{kpi:,.2f}")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Top 10 Produtos por Vendas")
    top_prod = (
        df_f.groupby("ProductName", as_index=False)["TotalDue"].sum()
        .sort_values("TotalDue", ascending=False)
        .head(10)
    )
    fig1, ax1 = plt.subplots(figsize=(8,5))
    ax1.bar(top_prod["ProductName"], top_prod["TotalDue"])
    ax1.set_xlabel("Produto")
    ax1.set_ylabel("Total de Vendas")
    ax1.tick_params(axis="x", rotation=45)
    st.pyplot(fig1, clear_figure=True)

with col2:
    st.subheader("Vendas ao longo do tempo (Ano-Mês)")
    sales_ts = (
        df_f.groupby("YearMonth", as_index=False)["TotalDue"].sum()
        .sort_values("YearMonth")
    )
    fig2, ax2 = plt.subplots(figsize=(8,5))
    ax2.plot(sales_ts["YearMonth"], sales_ts["TotalDue"], marker="o")
    ax2.set_xlabel("Período")
    ax2.set_ylabel("Total de Vendas")
    ax2.tick_params(axis="x", rotation=45)
    ax2.grid(True)
    st.pyplot(fig2, clear_figure=True)
