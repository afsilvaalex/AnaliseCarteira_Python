import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
import numpy as np
import random
from random import sample
sns.set()

# Selecionar os ativos desejados
#tickers_ibov = "ABEV3.SA AZUL4.SA B3SA3.SA BBAS3.SA BBDC3.SA BBDC4.SA BBSE3.SA ITUB4.SA IRBR3.SA  MGLU3.SA PETR4.SA"
tickers_ibov = "B3SA3.SA VALE3.SA JBSS3.SA"
dados_yahoo = yf.download(tickers_ibov, period='1y')["Adj Close"]

# Selecionar o indice ibovespa para comparacao
ibov = yf.download('BOVA11.SA', period='1y')["Adj Close"]
ibov = ibov / ibov.iloc[0]


# Retirar linhas e ativos que nao possuem informacoes completas
dados_yahoo.dropna(how='all', inplace=True)
dados_yahoo.dropna(axis=1, inplace=True, thresh=len(dados_yahoo))

# Transformar as variacoes em percentuais de cada ativo
retorno = dados_yahoo.pct_change()

# Criar um retorno acumulado do periodo considerando retorno desde o primeiro dia
# onde o primeiro dia é igual a 1
retorno_aculado = (1 + retorno).cumprod()
retorno_aculado.iloc[0] = 1

# configuracao das carteiras
valor_para_investir = 1500
qtd_de_ativos_carteira = 3
qtd_geracao_carteiras = 3

# auxiliares para selecionar a melhor carteira
maior_saldo = 0.0
melhor_carteira = []
colunas = []
selecao_igual = True

# Sorteio das carteiras aleatoria

carteira = dados_yahoo.columns

# valor em cada carteira
carteira = (valor_para_investir / qtd_de_ativos_carteira) * \
    retorno_aculado.loc[:, carteira]

# criar a coluna com o saldo somado com o fechamento do dia
carteira['saldo'] = carteira.sum(axis=1)
carteira['saldo'].plot(figsize=(18, 8))


# Plotar o indice do ibovespa no grafico
(ibov * valor_para_investir).plot(linewidth=4, color='black')

# Mostrar a melhor carteira
plt.title(str(melhor_carteira))
print("-------------- Carteira ----------------")
print(carteira.iloc[len(carteira)-1])
print("-----------------------------------------------")

plt.show()
