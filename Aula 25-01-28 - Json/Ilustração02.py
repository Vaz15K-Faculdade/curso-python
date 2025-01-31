import json

with open('ilustracao02.json', 'r') as f:

    for usuario in json.load(f):
        print(f"{usuario["nome"]} - {usuario["email"]}")