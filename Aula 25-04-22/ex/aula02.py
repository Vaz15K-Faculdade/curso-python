"""
    O que é Seaborn?

        Biblioteca de visualização baseada em Matplotlib.
        Foco em gráficos estatísticos e estética automática.

    Vantagens:
        Integração com DataFrames do Pandas.
        Temas e paletas de cores pré-definidas.
        Funções de alto nível para gráficos complexos.
"""

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Carregar dataset de exemplo (dados de gorjetas)
dados = sns.load_dataset("tips")
print(dados)

# Configurar tema visual
sns.set_theme(style="darkgrid", palette="pastel")

# ------------------------------------------------------------
# GRÁFICOS BÁSICOS:
# ------------------------------------------------------------

# Line Plot: Mostra tendências ao longo de um eixo contínuo (normalmente tempo)
# Aqui com média das gorjetas por valor da conta
sns.lineplot(data=dados, x="total_bill", y="tip", estimator="mean")
plt.savefig('00_lineplot.png')
plt.close()

# Histograma: Distribuição de frequências de uma variável numérica
# KDE=True adiciona curva de densidade
sns.histplot(data=dados, x="total_bill", kde=True)
plt.savefig('00_histplot.png')
plt.close()

# KDE Plot: Versão suavizada do histograma (estimativa de densidade)
sns.kdeplot(data=dados, x="total_bill")
plt.savefig('00_kdeplot.png')
plt.close()

# Count Plot: Contagem de observações por categoria
sns.countplot(data=dados, x="sex")
plt.savefig('00_countplot.png')
plt.close()

# ------------------------------------------------------------
# GRÁFICOS DE RELAÇÃO:
# ------------------------------------------------------------

# Scatter Plot: Relação entre duas variáveis numéricas
# Hue=time diferencia cores por período (almoço/jantar)
sns.scatterplot(data=dados, x="total_bill", y="tip", hue="time")
plt.savefig('00_scatterplot.png')
plt.close()

# Reg Plot: Scatter plot + linha de regressão (mostra tendência)
sns.regplot(data=dados, x="total_bill", y="tip")
plt.savefig('00_regplot.png')
plt.close()

# ------------------------------------------------------------
# GRÁFICOS DE COMPARAÇÃO:
# ------------------------------------------------------------

# Bar Plot: Comparação de médias entre categorias
# Hue=sex divide cada barra em subgrupos
sns.barplot(data=dados, x="day", y="total_bill", hue="sex", palette="rocket")
plt.title("Total da Conta por Dia e Sexo")
plt.xlabel("Dia da Semana")
plt.ylabel("Total ($)")
plt.savefig('00_barplot.png')
plt.close()

# Boxplot: Distribuição estatística (quartis, outliers)
# Mostra mediana, dispersão e valores extremos
sns.boxplot(data=dados, x="day", y="total_bill")
plt.savefig('00_boxplot.png')
plt.close()

# Violinplot: Combinação de boxplot + densidade (KDE)
sns.violinplot(data=dados, x="day", y="total_bill", hue="smoker")
plt.savefig('00_violinplot.png')
plt.close()

# ------------------------------------------------------------
# GRÁFICOS MULTIVARIADOS:
# ------------------------------------------------------------

# Heatmap: Representação matricial com cores (para dados tabulares/correlações)
dados_numericos = dados.select_dtypes(include=['float64', 'int64'])
sns.heatmap(dados_numericos)
plt.savefig('00_heatmap.png')
plt.close()

# PairPlot: Matriz de scatter plots para todas combinações de variáveis
sns.pairplot(dados, hue="time")
plt.savefig('00_pairplot.png')
plt.close()

# FacetGrid: Grid de gráficos divididos por categorias
grid = sns.FacetGrid(dados, col="time", row="smoker")
grid.map(sns.scatterplot, "total_bill", "tip")
plt.savefig('00_facetgrid.png')
plt.close()