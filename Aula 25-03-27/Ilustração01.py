import sqlite3

arquivo_banco = sqlite3.connect("banco_sql_python.db")

banco = arquivo_banco.cursor()

query = """
    UPDATE
        Aluno
    SET
        nota_1 = ?
    WHERE
        id = ?
"""

id = int(input("Digite o id do aluno: "))
nota_1 = float(input("Digite a nova nota 1: "))

banco.execute(query, (nota_1, id))
arquivo_banco.commit()