import sqlite3

arquivo_banco = sqlite3.connect("banco_sql_python.db")

banco = arquivo_banco.cursor()

query = """
    DELETE FROM
        Aluno
    WHERE
        id = ?
"""

id = int(input("Digite o id do aluno para deletar: "))

banco.execute(query, (id,))
arquivo_banco.commit()