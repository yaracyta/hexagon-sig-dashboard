import pandas as pd
ARQUIVO = "query.xlsx"
df = pd.read_excel(ARQUIVO)
df["OrderDate"] = pd.to_datetime(df["OrderDate"], errors="coerce")
df = df.dropna(subset=["OrderDate"])
vendas_regiao_produto = (
    df.groupby(["Region", "ProductName"], as_index=False)["TotalDue"].sum()
)
df["Ano"] = df["OrderDate"].dt.year
df["Mes"] = df["OrderDate"].dt.month
vendas_tempo = (
    df.groupby(["Ano", "Mes"], as_index=False)["TotalDue"].sum()
)
inicio = "2011-01-01"
fim = "2011-12-31"
filtro_datas = df[(df["OrderDate"] >= inicio) & (df["OrderDate"] <= fim)]
filtro_produto = df[df["ProductName"] == "Sport-100 Helmet, Red"]
filtro_regiao = df[df["Region"] == 79]
vendas_regiao_produto.to_excel("resumo_regiao_produto.xlsx", index=False)
vendas_tempo.to_excel("resumo_tempo.xlsx", index=False)
filtro_datas.to_excel("filtro_datas.xlsx", index=False)
filtro_produto.to_excel("filtro_produto.xlsx", index=False)
filtro_regiao.to_excel("filtro_regiao.xlsx", index=False)
print("✅ Arquivos Excel gerados com sucesso!")

# gráficos

import matplotlib.pyplot as plt
vendas_por_produto = (
    df.groupby("ProductName", as_index=False)["TotalDue"].sum()
    .sort_values("TotalDue", ascending=False)
)

plt.figure(figsize=(10,6))
plt.bar(vendas_por_produto["ProductName"], vendas_por_produto["TotalDue"])
plt.xticks(rotation=90)
plt.xlabel("Product")
plt.ylabel("Total Sales")
plt.title("Total Sales by Product")
plt.tight_layout()
plt.show()
vendas_tempo = (
    df.groupby(["Ano", "Mes"], as_index=False)["TotalDue"].sum()
    .sort_values(["Ano","Mes"])
)
vendas_tempo["Periodo"] = vendas_tempo["Ano"].astype(str) + "-" + vendas_tempo["Mes"].astype(str)

plt.figure(figsize=(10,6))
plt.plot(vendas_tempo["Periodo"], vendas_tempo["TotalDue"], marker="o")
plt.xticks(rotation=45)
plt.xlabel("Period (Year-Month)")
plt.ylabel("Total Sales")
plt.title("Sales Over Time")
plt.tight_layout()
plt.show()

import matplotlib.pyplot as plt
top_produtos = (
    df.groupby("ProductName", as_index=False)["TotalDue"].sum()
    .sort_values("TotalDue", ascending=False)
    .head(10)  # só os 10 maiores
)

plt.figure(figsize=(10,6))
plt.bar(top_produtos["ProductName"], top_produtos["TotalDue"], color="skyblue")
plt.xticks(rotation=45, ha="right")
plt.xlabel("Produto")
plt.ylabel("Total de Vendas")
plt.title("Top 10 Produtos por Vendas")
plt.tight_layout()
plt.show()
vendas_ano = df.groupby("Ano", as_index=False)["TotalDue"].sum()

plt.figure(figsize=(8,5))
plt.plot(vendas_ano["Ano"], vendas_ano["TotalDue"], marker="o", linestyle="-", color="green")
plt.xlabel("Ano")
plt.ylabel("Total de Vendas")
plt.title("Vendas ao longo dos anos")
plt.grid(True)
plt.tight_layout()
plt.show()


