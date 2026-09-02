"""
AULA 1 - Dados ausentes (parte curta)
Diagnosticar com isnull(), tratar com fillna() e dropna().
"""

import pandas as pd

# ---------------------------------------------------------------
# 1. DIAGNOSTICANDO: QUANTOS VALORES FALTAM, E ONDE (slide 7)
# ---------------------------------------------------------------
print("1. DIAGNÓSTICO - pacientes.isnull().sum()")

pacientes = pd.read_csv("pacientes.csv")
print(pacientes.isnull().sum())
# isnull() devolve uma tabela de True/False do mesmo tamanho do DataFrame;
# .sum() conta os True por coluna (True vale 1 nessa soma).
# Saída esperada: idade 0, telefone 12, convenio 47, peso 3.

print("\n--- percentual de ausentes por coluna ---")
print((pacientes.isnull().mean() * 100).round(0))
# isnull().mean() dá a fração de vazios; * 100 vira porcentagem.

print(pacientes.describe())

# ---------------------------------------------------------------
# 2. fillna() E dropna() NA PRÁTICA (slide 9)
# ---------------------------------------------------------------
print("2. fillna() COM MEDIANA + dropna(subset=)")


pacientes["peso"] = pacientes["peso"].fillna(
    pacientes["peso"].median()
)
pacientes_completos = pacientes.dropna(subset=["idade"])
print(pacientes_completos.shape)
# Saída esperada: (203, 5)
#
# fillna() troca o vazio no lugar (aqui precisou reatribuir a coluna) e
# PRESERVA o número de linhas.
# dropna(subset=["idade"]) remove linhas, mas SÓ olhando a coluna "idade".
# Sem subset, dropna() removeria qualquer linha com vazio em qualquer
# coluna - e aqui isso apagaria as 47 linhas sem "convenio", dado demais.
print("\nlinhas antes do dropna:", len(pacientes))
print("linhas depois do dropna:", len(pacientes_completos))

# Preenchendo a coluna categórica com uma categoria fixa:
pacientes_completos = pacientes_completos.copy()
pacientes_completos["convenio"] = pacientes_completos["convenio"].fillna("Particular")
print("\nnulos em convenio agora:", pacientes_completos["convenio"].isnull().sum())

# ---------------------------------------------------------------
# CHECKPOINT (slide 13)
# - isnull().sum()  -> diagnostica: quantos vazios e onde
# - fillna(media)   -> numérica sem outliers
# - fillna(mediana) -> numérica com outliers (não é puxada por extremos)
# - fillna("texto") -> categórica
# - dropna(subset=) -> poucos vazios em dado crítico
# ---------------------------------------------------------------

# ===============================================================
# DESAFIO RÁPIDO: NOTAS DE ALUNOS (slide 12)
# ===============================================================
# Uma escola tem 8 alunos sem nota de "prova final" registrada
# (ainda vão fazer segunda chamada). 

print("\n\nDESAFIO - notas_prova_final.csv")
notas_alunos = pd.read_csv("notas_prova_final.csv")
#print(notas_alunos)
print(notas_alunos.isnull().sum())
# Esperado: 8 vazios em "prova_final", 0 nas demais colunas.

media_real = notas_alunos["prova_final"].mean()          # ignora os NaN
media_com_zero = notas_alunos["prova_final"].fillna(0).mean()
print(f"\nmédia da prova final ignorando ausentes: {media_real:.2f}")
print(f"média se preenchêssemos com 0:          {media_com_zero:.2f}")
# Preencher com 0 uma prova que ainda NÃO existe distorce a média da turma
# para baixo, como se esses alunos tivessem tirado zero.
# Resposta certa: NÃO é fillna(0) nem preencher com a média agora - é
# esperar a segunda chamada, ou excluir esses alunos do cálculo até lá.