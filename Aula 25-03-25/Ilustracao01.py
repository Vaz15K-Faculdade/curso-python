import sqlite3

# Gerencia o banco de dados em si
con = sqlite3.connect("banco_sql_python.db")

# Gerencia o acesso ao SGDB, Requisições (select, insert, delete, etc...)
banco = con.cursor()

resultado = banco.execute("SELECT id, nome, turma FROM Aluno")
# alunos = resultado.fetchall() # Pega tudo
# alunos = resultado.fetchone() # Pega somente o primeiro
# Se eu continuar chamando, ele continuara pegando o proximo

alunos = resultado.fetchmany(5) # Pega quantos voce mandar...
print("Primeiro lote de alunos")
for id, nome, turma in alunos:
    print(f"{id} - {nome} - {turma}")

alunos = resultado.fetchmany(8)
print("Segundo lote de alunos")
for id, nome, turma in alunos:
    print(f"{id} - {nome} - {turma}")


""" # Um fetchall so que manual
while (aluno := resultado.fetchone()) is not None:
    print(aluno)
"""