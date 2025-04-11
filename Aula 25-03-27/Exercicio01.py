import sqlite3
import os

db_file = "banco_alunos.db"

if os.path.exists(db_file):
    conn = sqlite3.connect(db_file)
else:
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    query = """
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            turma TEXT,
            idade INTEGER,
            dta_nasc TEXT
        )
    """
    conn.execute(query)

cursor = conn.cursor()


def mostrar_alunos():
    query = """
        SELECT
            *
        FROM
            alunos
    """

    alunos = cursor.execute(query).fetchall()
    for aluno in alunos:
        print(f"{aluno}")


def criar_aluno():
    nome = input("Informe o nome do aluno: ")
    turma = input("Informe a Turma: ")
    idade = int(input("Informe a Idade: "))
    data = input("Informe a Data de nascimento: ")

    dicio = {
        "nome": nome,
        "turma": turma,
        "idade": idade,
        "dta_nasc": data
    }

    query = """
        INSERT INTO alunos (nome, turma, idade, dta_nasc)
        VALUES (:nome, :turma, :idade, :dta_nasc)
    """

    cursor.execute(query, dicio)
    conn.commit()

    novo_id = cursor.lastrowid
    print(f"Aluno criado com sucesso! ID: {novo_id}")


def atualizar_aluno():
    id = int(input("Informe o ID da pessoa: "))

    query = """
        SELECT
            *
        FROM
            alunos
        WHERE
            id = ?
    """

    aluno = conn.execute(query, (id,)).fetchall()
    if aluno:
        while True:
            print("1 - Nome\n",
                "2 - Turma\n",
                "3 - Idade\n",
                "4 - Data Nascimento")
            sel = int(input("O que deseja atualizar? "))

            if sel == 1:
                nome = input("Informe o nome do aluno: ")
                conn.execute("UPDATE alunos SET nome = ? WHERE id = ?", (nome, id))
                break
            elif sel == 2:
                turma = input("Informe a Turma: ")
                conn.execute("UPDATE alunos SET turma = ? WHERE id = ?", (turma, id))
                break
            elif sel == 3:
                idade = int(input("Informe a Idade: "))
                conn.execute("UPDATE alunos SET idade = ? WHERE id = ?", (idade, id))
                break
            elif sel == 4:
                data = input("Informe a Data de nascimento: ")
                conn.execute("UPDATE alunos SET dta_nasc = ? WHERE id = ?", (data, id))
                break
            else:
                print("Opção Invalida...")
        
        conn.commit()
        print("Atualização Completa!!")
    else:
        print(f"Nenhum aluno encontrado com o ID {id}")


def deletar_aluno():
    id = int(input("Informe o id que deseja excluir: "))

    query = """
        DELETE FROM
            alunos
        WHERE
            id = ?
    """

    conn.execute(query, (id,))

    conn.commit()
    print("Excluido!")


while True:
    print("1 - Mostrar Alunos\n",
        "2 - Inserir Novo Aluno\n",
        "3 - Atualizar Aluno por ID\n",
        "4 - Deletar Aluno por ID\n",
        "0 - Sair",
        )
    opc = int(input("Informe a opção Desejada: "))

    match opc:
        case 1:
            mostrar_alunos()
        case 2:
            criar_aluno()
        case 3:
            atualizar_aluno()
        case 4:
            deletar_aluno()
        case 0:
            print("Saindo...")
            break
