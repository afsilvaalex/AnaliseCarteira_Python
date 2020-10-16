import requests
import numpy as np
import pandas as pd
import string
import warnings
warnings.filterwarnings('ignore')


# proxies = {
#  "http": "http://10.10.1.10:3128",
#  "https": "http://10.10.1.10:1080",
# }

#requests.get("http://example.org", proxies=proxies)

url = 'http://fundamentus.com.br/resultado.php'

header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}

r = requests.get(url, headers=header)

# realizar leitura do primeiro data frame e normalizar . e ,
df = pd.read_html(r.text, decimal=',', thousands='.')[0]

# Normalizacao das colunas e transformar em float com decimal nas %
for coluna in ['Div.Yield', 'Mrg Ebit', 'Mrg. Líq.', 'ROIC', 'ROE', 'Cresc. Rec.5a']:
    df[coluna] = df[coluna].str.replace('.', '')
    df[coluna] = df[coluna].str.replace(',', '.')
    df[coluna] = df[coluna].str.rstrip('%').astype('float') / 100

# pegando as empresas com liquidez maior de 1MM
df = df[df['Liq.2meses'] > 1000000]

# gerar ranking das 150 empresas e calcular a formula magica
ranking = pd.DataFrame()
ranking['pos'] = range(1, 151)
ranking['EV/EBIT'] = df[df['EV/EBIT'] >
                        0].sort_values(by=['EV/EBIT'])['Papel'][:150].values
ranking['ROIC'] = df.sort_values(by=['ROIC'], ascending=False)[
    'Papel'][:150].values

# criar a visao EV/EBIT e visao ROIC com pivo_table
a = ranking.pivot_table(columns='EV/EBIT', values='pos')
b = ranking.pivot_table(columns='ROIC', values='pos')

# concatanar e excluir ativos que nao possui informacao e somar os rankings
t = pd.concat([a, b])
rank = t.dropna(axis=1).sum()

# mostrar as 15 primeiras
print(rank.sort_values()[:15])
