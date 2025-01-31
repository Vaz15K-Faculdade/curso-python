import json

with open('ilustracao01.json', 'r') as f:
    data = json.load(f)
    
    print(f"Bem vindo {data['user']}!")

    # print (f"Bem-vindo {json.load(f)['user']}!")
    