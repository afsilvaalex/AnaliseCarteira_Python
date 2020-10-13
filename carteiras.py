import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
import numpy as np
import random
from random import sample
sns.set()


# -----------------Configuracao para simulacao
# Selecionar os ativos desejados
#tickers_ibov = "ABEV3.SA AZUL4.SA B3SA3.SA BBAS3.SA BBDC3.SA BBDC4.SA BBSE3.SA ITUB4.SA IRBR3.SA  MGLU3.SA PETR4.SA"
#tickers_ibov = "BEEF3.SA CPLE6.SA SAPR11.SA WEGE3.SA TIMP3.SA VIVA3.SA FLRY3.SA MOVI3.SA USIM5.SA CIEL3.SA ITUB4.SA BBDC4.SA SANB11.SA BBSE3.SA PETR4.SA BRDT3.SA IRBR3.SA UGPA3.SA FLRY3.SA ODPV3.SA AZUL4.SA LAME4.SA VVAR3.SA"
tickers_ibov = "BBAS3.SA VVAR3.SA LWSA3.SA LAME4.SA GGBR4.SA OMGE3.SA MRFG3.SA VIVA3.SA B3SA3.SA VALE3.SA"
# Inclua os valores
valor_para_investir = 1500
qtd_de_ativos_carteira = 3
qtd_geracao_carteiras = 2000
tempo_de_simulacao = "2y"


dados_yahoo = yf.download(tickers_ibov, period=tempo_de_simulacao)["Adj Close"]

# Selecionar o indice ibovespa para comparacao
ibov = yf.download('BOVA11.SA', period=tempo_de_simulacao)["Adj Close"]
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


# auxiliares para selecionar a melhor carteira
maior_saldo = 0.0
melhor_carteira = []
colunas = []
selecao_igual = True

# Sorteio das carteiras aleatoria
for i in range(qtd_geracao_carteiras):
    # sorteio de carteiras sem repeticao
    carteira = []
    selecao_igual = True

    # nao deixar a carteira repetir o mesmo ativo
    while selecao_igual == True:
        carteira = random.choices(
            dados_yahoo.columns, k=qtd_de_ativos_carteira)
        colunas = list(set(carteira))
        if len(colunas) == len(carteira):
            selecao_igual = False

    # valor em cada carteira
    carteira = (valor_para_investir / qtd_de_ativos_carteira) * \
        retorno_aculado.loc[:, carteira]

    # criar a coluna com o saldo somado com o fechamento do dia
    carteira['saldo'] = carteira.sum(axis=1)
    carteira['saldo'].plot(figsize=(18, 8))

    # selecionar o ultimo dia da carteira para ver o saldo final e verificar se e a melhor opcao
    ultimoDia = carteira.iloc[len(carteira)-1]
    if ultimoDia['saldo'] > maior_saldo:
        maior_saldo = ultimoDia['saldo']
        melhor_carteira = ultimoDia

# Plotar o indice do ibovespa no grafico
(ibov * valor_para_investir).plot(linewidth=4, color='black')

# Mostrar a melhor carteira
plt.title(str(melhor_carteira))
print("-------------- Melhor Carteira ----------------")
print(melhor_carteira)
print("-----------------------------------------------")

plt.show()
