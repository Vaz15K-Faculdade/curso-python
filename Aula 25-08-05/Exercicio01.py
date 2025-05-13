#
# faça as seguintes classes:
# classe Pessoa, com atributos: 
#   - nome
#   - cpf
#
class Pessoa:
    def __init__(self, nome, cpf):
        self.nome= nome
        self.cpf = cpf

    def detalhes(self):
        print(f"Nome: {self.nome}")
        print(f"CPF: {self.cpf}")

# classe Estudante que herda de Pessoa, com atributos:
#   - curso
#   - semestre
#
class Estudante(Pessoa):
    def __init__(self, nome, cpf, curso, semestre):
        super().__init__(nome, cpf)
        self.curso = curso
        self.semestre = semestre

    def detalhes(self):
        super().detalhes()
        print(f"Curso: {self.curso}")
        print(f"Semestre: {self.semestre}")

# classe Professor que herda de Pessoa, com atributos:
#   - graduacao
#   - materia
# 
class Professor(Pessoa):
    def __init__(self, nome, cpf, graduacao, materia):
        super().__init__(nome, cpf)
        self.graduacao = graduacao
        self.materia = materia

    def detalhes(self):
        super().detalhes()
        print(f"Graduação: {self.graduacao}")
        print(f"Materia: {self.materia}")

# classe Monitor que herda de Estudante, com atributos:
#   - materia
#   - bolsa
#
class Monitor(Estudante):
    def __init__(self, nome, cpf, curso, semestre, materia, bolsa):
        super().__init__(nome, cpf, curso, semestre)
        self.materia = materia
        self.bolsa = bolsa

    def detalhes(self):
        super().detalhes()
        print(f"Materia: {self.materia}")
        print(f"Bolsa: {self.bolsa}")

# Todas as classes devem ter um método detalhes() que mostra 
# os atributos do objeto. Os atributos devem ser inicializados 
# através do construtor
#
# No método detalhes de cada sub-classe, chame o método detalhes() 
# do super para mostrar os atributos herdados
# opção 1: super().detalhes()
# opção 2: Pessoa.detalhes(self)

arthur = Monitor("Arthur", "123456789", "ADS", 2, "Python", 1000)
arthur.detalhes()

print()

Rodrigo = Professor("Rodrigo", "987654321", "Engenharia", "Matematica")
Rodrigo.detalhes()
