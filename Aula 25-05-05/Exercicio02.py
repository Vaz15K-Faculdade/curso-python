from Exercicio01 import Pessoa, Estudante, Professor, Monitor

class Registro():
    def __init__(self):
        self.pessoas = []
        self.estudantes = []
        self.professores = []
        self.monitores = []

    def registrar_pessoa(self):
        nome = input("Informe o nome da Pessoa: ")
        cpf = input("Informe o CPF da Pessoa: ")

        self.pessoas.append(Pessoa(nome, cpf))

    def registar_estudante(self):
        nome = input("Informe o nome do Estudante: ")
        cpf = input("Informe o CPF do Estudante: ")
        curso = input("Informe o Curso do Estudante: ")
        semestre = input("Informe o Semestre do Estudante")

        self.estudantes.append(Estudante(nome, cpf, curso, semestre))

    def registar_monitor(self):
        nome = input("Informe o nome do Monitor: ")
        cpf = input("Informe o CPF do Monitor: ")
        curso = input("Informe o Curso do Monitor: ")
        semestre = input("Informe o Semestre do Monitor")
        materia = input("Informe a Materia do Monitor: ")
        bolsa = input("Informe o valor da Bolsa do Monitor: ")

        self.monitores.append(Monitor(nome, cpf, curso, semestre, materia, bolsa))

    def registar_professores(self):
        nome = input("Informe o nome do Professor: ")
        cpf = input("Informe o CPF do Professor: ")
        graduacao = input("Informe o Graduação do Professor: ")
        Materia = input("Informe o Materia do Professor: ")

        self.professores.append(Professor(nome, cpf, graduacao, Materia))


registro = Registro()
while True:
    print("1 - Registrar Pessoa")
    print("2 - Registrar Estudante")
    print("3 - Registrar Professor")
    print("4 - Registrar Monitor")
    print("5 - Listar tudo")
    print("6 - Sair")
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        registro.registrar_pessoa()
    elif opcao == "2":
        registro.registar_estudante()
    elif opcao == "3":
        registro.registar_professores()
    elif opcao == "4":
        registro.registar_monitor()
    elif opcao == "5":
        print("Pessoas:")
        for pessoa in registro.pessoas:
            pessoa.detalhes()
            print()
        print("Estudantes:")
        for estudante in registro.estudantes:
            estudante.detalhes()
            print()
        print("Professores:")
        for professor in registro.professores:
            professor.detalhes()
            print()
        print("Monitores:")
        for monitor in registro.monitores:
            monitor.detalhes()
            print()
    elif opcao == "6":
        break
