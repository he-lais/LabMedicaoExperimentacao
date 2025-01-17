import requests
import json
import pandas as pd

url = 'https://api.github.com/graphql'
query = """query estrelas {
  search(type: REPOSITORY, first: 5, query: "stars:=>0") {
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
headers = {'Authorization': 'bearer 73af344f4d09bd6552ba2a68c80981a4146328a2'}

def executar_requisicao(url, query, header): 
    request = requests.post(url, json={'query': query}, headers=header)

    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("falha na requisição com código {}. {}".format(request.status_code, query))

resposta = executar_requisicao(url, query, headers)
print(resposta)