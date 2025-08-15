# Salve este arquivo como app.py e rode com: streamlit run app.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="Dashboard de Vendas", layout="wide")

# -----------------------
# Título
# -----------------------
st.title("Dashboard de Vendas - Loja Online")
st.markdown("Análise interativa de vendas, produtos e clientes.")

# -----------------------
# Gerar dados fictícios
# -----------------------
n_pedidos = 500
produtos = ['Camiseta', 'Calça', 'Tênis', 'Boné', 'Mochila', 'Jaqueta', 'Meias', 'Relógio', 'Óculos', 'Carteira']
clientes = [f'Cliente_{i}' for i in range(1, 51)]

def random_date(start, end):
    delta = end - start
    random_days = random.randrange(delta.days)
    return start + timedelta(days=random_days)

data_inicio = datetime(2025, 1, 1)
data_fim = datetime(2025, 7, 31)

dados = []
for i in range(1, n_pedidos + 1):
    pedido = {
        'OrderID': i,
        'CustomerID': random.choice(clientes),
        'Product': random.choice(produtos),
        'Quantity': random.randint(1, 5),
        'Price': round(random.uniform(10, 200), 2),
        'OrderDate': random_date(data_inicio, data_fim)
    }
    dados.append(pedido)

df = pd.DataFrame(dados)
df['OrderDate'] = pd.to_datetime(df['OrderDate'])
df['Month'] = df['OrderDate'].dt.month

# -----------------------
# Filtros interativos
# -----------------------
st.sidebar.header("Filtros")
produtos_selecionados = st.sidebar.multiselect("Produtos", produtos, default=produtos)
meses_selecionados = st.sidebar.multiselect("Meses", list(range(1,13)), default=list(range(1,13)))

df_filtrado = df[df['Product'].isin(produtos_selecionados) & df['Month'].isin(meses_selecionados)]

# -----------------------
# Métricas principais
# -----------------------
st.subheader("Métricas Principais")
col1, col2, col3 = st.columns(3)
col1.metric("Total de Pedidos", df_filtrado['OrderID'].nunique())
col2.metric("Total de Produtos Vendidos", df_filtrado['Quantity'].sum())
col3.metric("Clientes Únicos", df_filtrado['CustomerID'].nunique())

# -----------------------
# Top Produtos
# -----------------------
st.subheader("Top Produtos")
produtos_mais_vendidos = df_filtrado.groupby('Product')['Quantity'].sum().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(10,5))
sns.barplot(x=produtos_mais_vendidos.index, y=produtos_mais_vendidos.values, palette='viridis', ax=ax)
ax.set_ylabel("Quantidade")
ax.set_xlabel("Produto")
plt.xticks(rotation=45)
st.pyplot(fig)

# -----------------------
# Top Clientes
# -----------------------
st.subheader("Top Clientes")
clientes_mais_frequentes = df_filtrado.groupby('CustomerID')['Quantity'].sum().sort_values(ascending=False)

fig2, ax2 = plt.subplots(figsize=(10,5))
sns.barplot(x=clientes_mais_frequentes.index[:10], y=clientes_mais_frequentes.values[:10], palette='plasma', ax=ax2)
ax2.set_ylabel("Quantidade")
ax2.set_xlabel("Cliente")
plt.xticks(rotation=45)
st.pyplot(fig2)

# -----------------------
# Vendas por mês
# -----------------------
st.subheader("Vendas por Mês")
vendas_por_mes = df_filtrado.groupby('Month')['Quantity'].sum()

fig3, ax3 = plt.subplots(figsize=(10,5))
sns.lineplot(x=vendas_por_mes.index, y=vendas_por_mes.values, marker='o', ax=ax3)
ax3.set_ylabel("Quantidade de Produtos Vendidos")
ax3.set_xlabel("Mês")
st.pyplot(fig3)

# -----------------------
# Mostrar tabela de dados
# -----------------------
st.subheader("Tabela de Dados Filtrada")
st.dataframe(df_filtrado.reset_index(drop=True))
