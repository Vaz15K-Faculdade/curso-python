class Pessoa:
    def __init__(self, nome, cpf):
        self.nome = nome
        self.cpf = cpf

    def descricao(self):
        print(f"Nome: {self.nome} - CPF: {self.cpf}")

class Professor(Pessoa):
    def __init__(self, nome, cpf, graduacao, materia):
        super().__init__(nome, cpf)
        self.graduacao = graduacao
        self.materia = materia

class Aluno(Pessoa):
    def __init__(self, nome, cpf, curso, semestre):
        super().__init__(nome, cpf)
        self.curso = curso
        self.semestre = semestre

p1 = Professor("João", "123456789-00", "Matemática", "Cálculo")
p2 = Aluno("Maria", "987654321-00", "Engenharia", 3)

p1.descricao()
p2.descricao()