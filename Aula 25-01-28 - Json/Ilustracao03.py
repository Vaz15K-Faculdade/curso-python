import json 

usuario = {
    '123.456.789-00': 'João',
    '987.654.321-00': 'Maria',
    '111.222.333-44': 'José'
}

with open('ilustracao03.json', 'w') as file:
    # Metodo 1
    json.dump(usuario, file, indent=4, ensure_ascii=False)

    # Metodo 2
    # file.write(json.dumps(usuario))