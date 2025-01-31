import requests

uf = input("Estado: ")
url = f'https://servicodados.ibge.gov.br/api/v1/localidades/estados/{uf}/distritos'

http_req = requests.get(url)

dados = http_req.json()

for cidade in dados:
    print(cidade['nome'])