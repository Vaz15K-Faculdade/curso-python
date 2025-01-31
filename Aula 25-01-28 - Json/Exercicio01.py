import json

cadastros = []

def cadastrar_pessoa():
    nome = input("Digite o nome: ")
    cpf = input("Digite o CPF: ")
    pessoa = {
        "cpf": cpf,
        "nome": nome
    }
    cadastros.append(pessoa)
    return pessoa

def listar_cadastros():
    for pessoa in cadastros:
        print(f"Nome: {pessoa['nome']}, CPF: {pessoa['cpf']}")

def salvar_cadastros():
    with open("cadastros.json", "w") as file:
        json.dump(cadastros, file, indent=4)

def carregar_cadastros():
    global cadastros
    with open("cadastros.json", "r") as file:
        cadastros = json.load(file)

while True:
    print("1 - Cadastrar Pessoa\n"
          "2 - Listar Cadastros\n"
          "3 - Salvar Cadastros\n"
          "4 - Carregar Cadastros\n"
          "5 - Sair")
    opcao = input("Selecione a opcao desejada: ")

    match opcao:
        case "1": 
            pessoa = cadastrar_pessoa()
            print("Pessoa cadastrada com sucesso!\n")
        case "2":
            listar_cadastros()
        case "3":
            salvar_cadastros()
            print("Cadastros salvos com sucesso!\n")
        case "4":
            carregar_cadastros()
            print("Cadastros carregados com sucesso!\n")
        case "5":
            print("Saindo do programa...\n")
            break
        case _:
            print("Opcao invalida!\n")
