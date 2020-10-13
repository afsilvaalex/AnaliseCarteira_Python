import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
import numpy as np
import random
from random import sample
sns.set()

# Valor de investimento para simulacao
valor_para_investir = 1500
tempo_comparacao_anos = '2y'

# Incluir a carteira 1 para compacao
tickers_ibov_carteira1 = "BBAS3.SA VVAR3.SA LWSA3.SA LAME4.SA GGBR4.SA OMGE3.SA MRFG3.SA VIVA3.SA B3SA3.SA VALE3.SA"
tickers_ibov_carteira2 = "LAME4.SA  VVAR3.SA WEGE3.SA"

dados_yahoo_carteira1 = yf.download(
    tickers_ibov_carteira1, period=tempo_comparacao_anos)["Adj Close"]

dados_yahoo_carteira2 = yf.download(
    tickers_ibov_carteira2, period=tempo_comparacao_anos)["Adj Close"]

# Selecionar o indice ibovespa para comparacao
ibov = yf.download('BOVA11.SA', period=tempo_comparacao_anos)["Adj Close"]
ibov = ibov / ibov.iloc[0]

# Retirar linhas e ativos que nao possuem informacoes completas carteira 1 e carteira 2
dados_yahoo_carteira1.dropna(how='all', inplace=True)
dados_yahoo_carteira1.dropna(
    axis=1, inplace=True, thresh=len(dados_yahoo_carteira1))

dados_yahoo_carteira2.dropna(how='all', inplace=True)
dados_yahoo_carteira2.dropna(
    axis=1, inplace=True, thresh=len(dados_yahoo_carteira2))

# Transformar as variacoes em percentuais de cada ativo
retorno_carteira1 = dados_yahoo_carteira1.pct_change()
retorno_carteira2 = dados_yahoo_carteira2.pct_change()

# Criar um retorno acumulado do periodo considerando retorno desde o primeiro dia
# onde o primeiro dia é igual a 1
retorno_acumulado_carteira1 = (1 + retorno_carteira1).cumprod()
retorno_acumulado_carteira1.iloc[0] = 1

retorno_acumulado_carteira2 = (1 + retorno_carteira2).cumprod()
retorno_acumulado_carteira2.iloc[0] = 1

# Calculo e plot da carteira 1

carteira1 = dados_yahoo_carteira1.columns

# valor em cada carteira
carteira1 = (valor_para_investir / len(carteira1)) * \
    retorno_acumulado_carteira1.loc[:, carteira1]
# criar a coluna com o saldo somado com o fechamento do dia
carteira1['saldo'] = carteira1.sum(axis=1)
carteira1['saldo'].plot(
    figsize=(18, 8), label=tickers_ibov_carteira1.replace(".SA", ""))


# Calculo e plot da carteira 2

carteira2 = dados_yahoo_carteira2.columns

# valor em cada carteira
carteira2 = (valor_para_investir / len(carteira2)) * \
    retorno_acumulado_carteira2.loc[:, carteira2]
# criar a coluna com o saldo somado com o fechamento do dia
carteira2['saldo'] = carteira2.sum(axis=1)
carteira2['saldo'].plot(
    figsize=(18, 8), label=tickers_ibov_carteira2.replace(".SA", ""))


# Plotar o indice do ibovespa no grafico
(ibov * valor_para_investir).plot(linewidth=2, color='black', label="IBOVESPA")

print("-------------- Carteira 1-----------------")
print(carteira1.iloc[len(carteira1)-1])
print("------------------------------------------")
print("-------------- Carteira 2-----------------")
print(carteira2.iloc[len(carteira2)-1])
print("------------------------------------------")


# configurar o grafico
plt.title("Comparação entre carteiras")
plt.ylabel('Retorno em R$')
plt.xlabel('Desempenho no tempo: ' + tempo_comparacao_anos)

plt.legend(loc='lower left')
plt.grid(True)
plt.show()
