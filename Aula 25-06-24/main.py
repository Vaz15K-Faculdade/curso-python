from PySide6.QtWidgets import *
from pathlib import Path

from janelaCadastro import Ui_Form
from mainWindow import Ui_MainWindow
from db import ConnDB

class JanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui= Ui_MainWindow()
        self.ui.setupUi(self)

        self.db = ConnDB(str((Path(__file__).resolve().parent / 'cadastros.db')))

        self.ui.actionAdicionar.triggered.connect(self.abrir_cadastro)
        self.ui.actionAdicionar.triggered.connect(self.abrir_alterar)
        
        self.janelaCadastro = JanelaCadastro(self)
        self.atualizar_tabela()

    def abrir_cadastro(self):
        self.janelaCadastro.modo_cadastro()

    def abrir_alterar(self):
        self.janelaCadastro.modo_alterar()

    def atualizar_tabela(self):
        dados = self.db.ler_cadastro()
        
        self.ui.tableWidget.setRowCount(len(dados))

        for linha, dado in enumerate(dados):
            self.ui.tableWidget.setItem(linha, 0, QTableWidgetItem(dado[1]))
            self.ui.tableWidget.setItem(linha, 0, QTableWidgetItem(dado[2]))
            self.ui.tableWidget.setItem(linha, 0, QTableWidgetItem(dado[3]))

    def cadastrar(self, nome, telefone, email):
        self.db.criar_cadastro(nome, telefone, email)
        self.atualizar_tabela()

class JanelaCadastro(QWidget):
    def __init__(self, janelaPrincipal):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.janelaPrincipal : JanelaPrincipal = janelaPrincipal

        self.ui.botaoOk.clicked.connect(self.aplicar)
        self.ui.botaoOk.clicked.connect(self.close)

    def modo_cadastro(self):
        self.setWindowTitle("Adicionar")
        self.ui.editNome.setText("")
        self.ui.editTelefone.setText("")
        self.ui.editEmail.setText("")
        self.show()
    
    def modo_alterar(self):
        self.setWindowTitle("Alterar")
        self.ui.editNome.setText("")
        self.ui.editTelefone.setText("")
        self.ui.editEmail.setText("")
        self.show()

    def aplicar(self):
        nome = self.ui.editNome.text()
        telefone = self.ui.editTelefone.text()
        email = self.ui.editEmail.text()

        self.janelaPrincipal.cadastrar(nome, telefone, email)
        self.close()

app = QApplication([])

janela = JanelaPrincipal()
janela.show()
app.exec()