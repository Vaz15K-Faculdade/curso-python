import requests 

headers = {
    'User-Agent' : 'Mozilla/5.0' 
}

url = 'https://statusinvest.com.br/acao/tickerprice'

params = {
    'ticker' : 'PETR4',
    'type': '1',
    'currences': '1'
}

http_req = requests.get(url, params=params, headers=headers)

dados = http_req.json()

for preco in dados[0]['prices']:
    print(f'{preco['date']} - {preco['price']}')
