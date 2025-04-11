import sqlite3

arquivo_db = sqlite3.connect("banco_sql_python.db")

banco = arquivo_db.cursor()

alunos = []

while True:
    nome = input("Digite o seu nome: ")
    turma = input("Digite sua turma: ")
    nota_1 = input("Digite a nota 1: ")
    nota_2 = input("Digite a nota 2: ")
    nota_3 = input("Digite a nota 3: ")
    nota_4 = input("Digite a nota 4: ")

    aluno = (nome, turma, nota_1, nota_2, nota_3, nota_4)
    alunos.append(aluno)

    if ((input("Deseja Continuar? S/N ")).lower() != "s"):
        break

banco.executemany("""
    INSERT INTO Aluno (nome, turma, nota_1, nota_2, nota_3, nota_4)
    VALUES (?, ?, ?, ?, ?, ?)
""",
alunos
)

arquivo_db.commit()