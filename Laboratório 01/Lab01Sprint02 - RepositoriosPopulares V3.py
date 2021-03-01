import requests
import json
import pandas as pd

url: str = 'https://api.github.com/graphql'

headers: str = {'Authorization': 'Bearer 73af344f4d09bd6552ba2a68c80981a4146328a2'}

query: str = """query estrelas {
  search(type: REPOSITORY, first: 10, after: {AFTER}, query: "stars:=>0") {
    pageInfo{      
      endCursor
    }
    nodes {
      ... on Repository {
        nome: nameWithOwner
        numeroEstrelas: stargazerCount
        dataCriacao: createdAt
        linguagemPrimaria: primaryLanguage {
          name
        }
        quantidadePullRequests: pullRequests(states: MERGED) {
          totalCount
        }
        quantidadeReleases: releases {
          totalCount
        }
        dataUltimaRelease: latestRelease {
          createdAt
        }
        totalOpenIssues: issues(states: CLOSED) {
          totalCount
        }
        totalIssues: issues {
          totalCount
        }
      }
    }
  }
}"""


def executar_requisicao(url: str, query: str, header: dict) -> dict: 
    request = requests.post(url, json={'query': query}, headers=header)

    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("falha na requisição com código {}. {}".format(request.status_code, query))

after: str = 'null'
resposta: dict = executar_requisicao(url, query.replace('{AFTER}', after), headers)
after: str = '"' + resposta['data']['search']['pageInfo']['endCursor'] + '"'

for i in range(2):
  aux: dict = executar_requisicao(url, query.replace('{AFTER}', after), headers)
  after: str = '"' + aux['data']['search']['pageInfo']['endCursor'] + '"'
  resposta.update(aux)

#criando arquivo .json, lendo e convertendo para Excel.
with open('resposta.json', 'w') as f:
    json.dump(resposta, f)

d: dict
with open('resposta.json', 'r') as f:
    d = json.load(f)

df: pd.DataFrame = pd.DataFrame.from_dict(d['data']['search']['nodes'])
df.to_csv('resposta.csv')
df.to_excel('resposta.xls')