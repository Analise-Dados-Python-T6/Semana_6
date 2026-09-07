"""
AULA 3 - Transformações 

"""

import numpy as np
import pandas as pd


print("apply(axis=1) EM seguros.csv")

seguros = pd.read_csv("seguros.csv")

def calcular_premio(linha):
    base = linha["valor_veiculo"] * 0.03
    if linha["idade"] < 25:
        base *= 1.4
    if linha["sinistros"] > 0:
        base *= 1.25
    return round(base, 2)

seguros["premio"] = seguros.apply(calcular_premio, axis=1)
print(seguros["premio"])



print("\n np.where EM clientes.csv")

clientes = pd.read_csv("clientes.csv")
clientes["categoria"] = np.where(
    clientes["total_gasto"] > 5000, "VIP", "Regular"
)
print(clientes["categoria"].value_counts())



print("\n concat DE TRÊS FILIAIS")

vendas_centro = pd.read_csv("vendas_centro.csv")
vendas_shopping = pd.read_csv("vendas_shopping.csv")
vendas_online = pd.read_csv("vendas_online.csv")

vendas_total = pd.concat(
    [vendas_centro, vendas_shopping, vendas_online],
    ignore_index=True,
)
print(vendas_total.shape)
print(vendas_total["filial"].value_counts())



print("\nLIMPANDO NOMES DE CLIENTES DE UM CRM")

clientes["nome"] = clientes["nome"].str.strip().str.title()
print(clientes["nome"].head(3).tolist())



print("\n8. to_numeric E to_datetime")

sensores = pd.read_csv("sensores.csv")
entregas = pd.read_csv("entregas.csv")

sensores["temperatura"] = pd.to_numeric(
    sensores["temperatura"], errors="coerce"
)
entregas["data"] = pd.to_datetime(
    entregas["data"], dayfirst=True
)
print(sensores["temperatura"].isnull().sum(), "leituras viraram NaN")
print(sensores["temperatura"])
print(entregas["data"])
print(entregas["data"].dt.strftime("%d/%m/%Y"))
