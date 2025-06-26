import sqlite3
from pathlib import Path

class ConnDB():
    def __init__(self, arquivoBanco):
        if Path(arquivoBanco).exists():
            self.conn = sqlite3.connect(arquivoBanco)
            self.cursor = self.conn.cursor()
        else:
            self.conn = sqlite3.connect(arquivoBanco)
            self.cursor = self.conn.cursor()

            self.cursor.execute("""
                CREATE TABLE cadastros (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT,
                    telefone TEXT,
                    email TEXT
                )
            """)
            self.conn.commit()
    
    def ler_cadastro(self):
        self.cursor.execute("SELECT * FROM cadastros")
        return self.cursor.fetchall()
    
    def criar_cadastro(self, nome, telefone, email):
        self.cursor.execute("""
            INSERT INTO cadastros (nome, telefone, email)
            VALUES (?, ?, ?)
        """, (nome, telefone, email))
        self.conn.commit()

    def remover_cadastro(self, id):
        self.cursor.execute("DELETE FROM cadastros WHERE id=?", (id,))
        self.conn.commit()

    def alterar_cadastro(self, id, nome, telefone, email):
        self.cursor.execute("""
            UPDATE cadastros
            SET nome=?, telefone=?, email=?
            WHERE id=?
        """, (nome, telefone, email, id))
        self.conn.commit()

    def fechar_conexao(self):
        self.conn.close()