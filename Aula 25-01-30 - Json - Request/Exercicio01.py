import json

try:
    with open("cadastros.json", "r") as file:
        cadastros = json.load(file)
except:
    cadastros = {}

def salvar_cadastros():
    with open("cadastros.json", "w") as file:
        json.dump(cadastros, file, indent=4)

def cadastrar_pessoa():
    nome = input("Digite o nome da pessoa: ")
    cpf = input("Digite o CPF da pessoa: ")
    if cpf in cadastros:
        print("CPF já cadastrado!")
        return
    email = input("Digite o email da pessoa: ")
    telefone = input("Digite o telefone da pessoa: ")
    
    pessoa = {"nome": nome,
              "cpf": cpf,
              "email": email,
              "telefone": telefone}
    cadastros[cpf] = pessoa
    salvar_cadastros()

def listar_cadastros():
    for cpf in cadastros:
        print(f"Nome: {cadastros[cpf]["nome"]}\n"
              f"CPF: {cadastros[cpf]["cpf"]}\n"
              f"Email: {cadastros[cpf]["email"]}\n"
              f"Telefone: {cadastros[cpf]["telefone"]}\n")

def editar_cadastro():
    cpf = input("Digite o cpf da pessoa que deseja editar: ")
    if cpf in cadastros:
        opcao = input("Selecione o campo que deseja editar:\n"
                        "1 - Nome\n"
                        "2 - CPF\n"
                        "3 - Email\n"
                        "4 - Telefone\n")
        if opcao == "1":
            cadastros[cpf]["nome"] = input("Digite o novo nome: ")
        elif opcao == "2":
            cadastros[cpf]["cpf"] = input("Digite o novo cpf: ")
        elif opcao == "3":
            cadastros[cpf]["email"] = input("Digite o novo email: ")
        elif opcao == "4":
            cadastros[cpf]["telefone"] = input("Digite o novo telefone: ")
        else:
            print("Opção inválida!")
        salvar_cadastros()
    else:
        print("CPF não encontrado!")

def excluir_cadastro():
    cpf = input("Digite o cpf da pessoa que deseja excluir: ")
    if cpf in cadastros:
        cadastros.pop(cpf)
        salvar_cadastros()
    else:
        print("CPF não encontrado!")

def procurar_cadastro():
    cpf = input("Digite o cpf da pessoa que deseja procurar: ")
    if cpf in cadastros:
        print(f"Nome: {cadastros[cpf]["nome"]}\n"
              f"CPF: {cadastros[cpf]["cpf"]}\n"
              f"Email: {cadastros[cpf]["email"]}\n"
              f"Telefone: {cadastros[cpf]["telefone"]}\n")
    else:
        print("CPF não encontrado!")

while True:
    opcao = input("Selecione a opção desejada:\n"
                "1 - Cadastrar Pessoa\n"
                "2 - Listar Cadastros\n"
                "3 - Editar Cadastro\n"
                "4 - Excluir Cadastro\n"
                "5 - Procurar Cadastro\n"
                "6 - Sair\n")
    
    match opcao:
        case "1":
            cadastrar_pessoa()
        case "2":
            listar_cadastros()
        case "3":
            editar_cadastro()
        case "4":
            excluir_cadastro()
        case "5":
            procurar_cadastro()
        case "6":
            print("Saindo do programa...")
            break
