import requests
import json
import pandas as pd

url = 'https://api.github.com/graphql'

headers = {'Authorization': 'bearer 73af344f4d09bd6552ba2a68c80981a4146328a2'}

query = """query java {
  search(type: REPOSITORY, first: 10{AFTER}, query: "stars:=>0 language:java") {
    pageInfo {
      endCursor
    }
    nodes {
      ... on Repository {
        nome: nameWithOwner
        numeroEstrelas: stargazerCount
        dataCriacao: createdAt
        url: url
        quantidadeReleases: releases {
          totalCount
        }
      }
    }
  }
}"""


def executar_requisicao(url, query, header): 
    request = requests.post(url, json={'query': query}, headers=header)

    if request.status_code == 200:
        return request.json()
    else:
        return 'falha'

after = ''
resposta = {'resp': []}
i = 0
while i < 100:
  aux = executar_requisicao(url, query.replace('{AFTER}', after), headers)
  if aux != 'falha':
    after = ', after: "' + aux['data']['search']['pageInfo']['endCursor'] + '"'
    i += 1
    resposta['resp'] += aux['data']['search']['nodes']

#criando arquivo .json, lendo e convertendo para Excel.
with open('resposta.json', 'w') as f:
    json.dump(resposta, f)

d: dict
with open('resposta.json', 'r') as f:
    d = json.load(f)

df: pd.DataFrame = pd.DataFrame.from_dict(d['resp'])
df.to_csv('resposta.csv')
df.to_excel('resposta.xls')

print('FIM DO PROCESSAMENTO')
