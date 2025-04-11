"""
Faça uma seleção dos alunos cuja nota_4 > 8
em seguida mostre os dados dos alunos retornados
"""

import sqlite3

arquivo_db = sqlite3.connect("banco_sql_python.db")

banco = arquivo_db.cursor()

sql_query = """
    SELECT
        *
    FROM
        Aluno
    WHERE
        nota_4 > 8
"""

resultado = banco.execute(sql_query)

alunos = resultado.fetchall()
for aluno in alunos:
    print(f"{aluno}")
