"""
AULA 2 - Limpeza de dados
Duplicatas (drop_duplicates), outliers (regra do IQR) e padronização (Z-score).
Slides 14 a 25 do deck "Semana 06 - Limpeza e Transformação de Dados".
"""

import pandas as pd

# ---------------------------------------------------------------
# 1. DUPLICATAS: O MESMO REGISTRO APARECE DUAS VEZES (slide 15)
# ---------------------------------------------------------------
# Duplicata = linhas idênticas (em todas as colunas ou só nas escolhidas).
# O parâmetro keep decide qual cópia sobrevive:
#   keep="first"  -> mantém a primeira ocorrência (padrão)
#   keep="last"   -> mantém a última
#   keep=False    -> remove todas as cópias (nem a primeira sobra)

# ---------------------------------------------------------------
# 2. CONSOLIDANDO PEDIDOS DUPLICADOS (slide 16)
# ---------------------------------------------------------------
print("2. DUPLICATAS EM pedidos.csv")

pedidos = pd.read_csv("pedidos.csv")
print(pedidos.duplicated().sum(), "linhas duplicadas")

pedidos_limpos = pedidos.drop_duplicates(keep="first")
print(len(pedidos), " ", len(pedidos_limpos))
# Saída esperada: 1248   1195  (53 duplicatas removidas)
#
# .duplicated() só MARCA (True/False) quais linhas são cópia de uma
# anterior, sem remover nada; por isso .sum() conta antes de agir.
# drop_duplicates() de fato remove e devolve um DataFrame novo.
# Por padrão a linha inteira é considerada; para duplicata parcial use
# drop_duplicates(subset=["coluna"]).

# ---------------------------------------------------------------
# 3. OUTLIERS: O VALOR QUE NÃO PARECE PERTENCER ALI (slide 19)
# ---------------------------------------------------------------
# Outlier NÃO é sinônimo de erro: é um valor real, mas estatisticamente
# distante da maioria. A regra do IQR (intervalo interquartil) é preferida
# à "desvios da média" porque não assume distribuição normal (curva de sino):
#   IQR = Q3 - Q1
#   limite inferior = Q1 - 1.5 * IQR
#   limite superior = Q3 + 1.5 * IQR

# ---------------------------------------------------------------
# 4. DETECTANDO IMÓVEIS FORA DO PADRÃO (slide 20)
# ---------------------------------------------------------------
print("\n4. OUTLIERS DE PREÇO EM imoveis.csv")

imoveis = pd.read_csv("imoveis.csv")
Q1 = imoveis["preco"].quantile(0.25)
Q3 = imoveis["preco"].quantile(0.75)
IQR = Q3 - Q1
limite_superior = Q3 + 1.5 * IQR
outliers = imoveis[imoveis["preco"] > limite_superior]
print(len(outliers), "imóveis fora do padrão")
# Saída esperada: 3 imóveis fora do padrão
#
# O filtro final usa a mesma sintaxe de filtro booleano já vista na Semana 05.
# Aqui só o limite SUPERIOR foi calculado; para outliers "baixos" seria
# preciso Q1 - 1.5 * IQR também.
# Atenção: outlier DETECTADO não é outlier REMOVIDO automaticamente -
# documentar a decisão é parte do processo.

# ---------------------------------------------------------------
# 5. PADRONIZAÇÃO: COLOCANDO TUDO NA MESMA ESCALA (slide 21)
# ---------------------------------------------------------------
# Z-score = (valor - média) / desvio padrão.
# O resultado diz quantos desvios padrão aquele valor está acima (+) ou
# abaixo (-) da média, permitindo comparar colunas com escalas diferentes
# (ex: nota 0-10 vs pontuação 0-1000) na mesma régua.
# Padronizar NÃO muda a posição relativa: quem era o maior continua o maior.

# ---------------------------------------------------------------
# 6. PADRONIZANDO NOTAS EM ESCALAS DIFERENTES (slide 22)
# ---------------------------------------------------------------
print("\n6. Z-SCORE EM notas.csv")

notas = pd.read_csv("notas.csv")
media = notas["pontuacao"].mean()
desvio = notas["pontuacao"].std()
notas["z_score"] = (notas["pontuacao"] - media) / desvio
print(notas[["aluno", "pontuacao", "z_score"]].head(3).round(2))
# Saída esperada (aprox.):
#     aluno  pontuacao  z_score
# 0     Ana        720     0.85
# 1   Bruno        540    -0.62
# 2   Carla        810     1.58
#
# A fórmula é aplicada de forma vetorizada (coluna inteira de uma vez, sem loop).
# z_score não tem a unidade da coluna original: não é mais "pontos", é "desvios padrão".

# ---------------------------------------------------------------
# CHECKPOINT (slide 24)
# - drop_duplicates(keep=) -> remove cópias indesejadas
# - IQR                    -> identifica outliers sem assumir distribuição normal
# - Z-score                -> padroniza colunas em escalas diferentes
# ---------------------------------------------------------------


# ===============================================================
# DESAFIO: DADOS DE UMA REDE DE ACADEMIAS (slide 23)
# ===============================================================
# Base de check-ins de uma rede de academias com:
#   - registros duplicados (o app às vezes grava o mesmo check-in 2x)
#   - sessões de treino com duração fora do padrão (ex: 800 min numa sessão)
#   - pontuação de desempenho em escalas diferentes entre as unidades
# Passos (a ORDEM importa: remover duplicatas ANTES de calcular o IQR
# evita que um check-in repetido conte como sessão a mais):
#   1) remover duplicatas com o keep adequado
#   2) usar IQR para achar as sessões com duração fora do padrão
#   3) padronizar a pontuação com Z-score PARA COMPARAR as unidades
#   4) apresentar quantos registros mudaram em cada etapa e por quê
print("\n\nDESAFIO - ginasio_checkins.csv")

checkins = pd.read_csv("ginasio_checkins.csv")
print("linhas lidas:", len(checkins))

# 1) duplicatas
n_dup = checkins.duplicated().sum()
checkins = checkins.drop_duplicates(keep="first").reset_index(drop=True)
print(f"duplicatas removidas: {n_dup}  ->  linhas agora: {len(checkins)}")

# 2) outliers de duração (regra do IQR, limites inferior e superior)
Q1 = checkins["duracao_min"].quantile(0.25)
Q3 = checkins["duracao_min"].quantile(0.75)
IQR = Q3 - Q1
limite_inf = Q1 - 1.5 * IQR
limite_sup = Q3 + 1.5 * IQR
fora_padrao = checkins[
    (checkins["duracao_min"] < limite_inf) | (checkins["duracao_min"] > limite_sup)
]
print(f"sessões com duração fora do padrão: {len(fora_padrao)} "
      f"(limites: {limite_inf:.0f} a {limite_sup:.0f} min)")

# 3) Z-score da pontuação POR unidade (cada unidade na sua própria régua)
checkins["z_desempenho"] = checkins.groupby("unidade")["pontuacao_desempenho"].transform(
    lambda s: (s - s.mean()) / s.std()
)
print("\nz-score de desempenho por unidade (primeiras linhas):")
print(checkins[["unidade", "pontuacao_desempenho", "z_desempenho"]].head().round(2))
