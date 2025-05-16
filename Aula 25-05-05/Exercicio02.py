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

    @staticmethod
    def listar(lista):
        for obj in lista:
            obj.detalhes()

    def listar_pessoas(self):
        Registro.listar(self.pessoas)

    def listar_estudantes(self):
        Registro.listar(self.estudantes)

    def listar_professores(self):
        Registro.listar(self.professores)

    def listar_monitores(self):
        Registro.listar(self.monitores)