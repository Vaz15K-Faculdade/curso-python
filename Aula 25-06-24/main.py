from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
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
        self.ui.actionAlterar.triggered.connect(self.abrir_alterar)

        self.ui.actionRemover.triggered.connect(self.remover)
        
        self.janelaCadastro = JanelaCadastro(self)
        self.atualizar_tabela()

    def abrir_cadastro(self):
        self.janelaCadastro.modo_cadastro()

    def abrir_alterar(self):
        linhas = self.ui.tableWidget.selectionModel().selectedRows()

        if linhas:
            if len(linhas) > 1:
                QMessageBox.warning(self, "Erro", "Selecione apenas uma linha para alterar")
            else:
                cadastro = self.get_cadastro(linhas[0].row())
                self.janelaCadastro.modo_alterar(cadastro)
    
    def get_cadastro(self, indice):
        return self.cadastros[indice]
    
    def alterar_cadastro(self, id, nome, telefone, email):
        self.db.alterar_cadastro(id, nome, telefone, email)
        self.atualizar_tabela()
    
    def remover(self):
        linhas = self.ui.tableWidget.selectionModel().selectedRows()

        if not linhas:
            QMessageBox.warning(self, "Erro", "Nenhuma Linhas Seleiconada!")
            return

        linhasRemovidas = ""
        for linha in linhas:
            #Remover o cadastro da referente a linha
            cadastro = self.get_cadastro(linha.row())
            linhasRemovidas += "\n" + str(cadastro)

        caixaConfirmar = QMessageBox()
        caixaConfirmar.setWindowTitle("Confimar Remoção")
        caixaConfirmar.setText(f"Remover as seguintes linhas: {linhasRemovidas}")
        caixaConfirmar.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        resultado = caixaConfirmar.exec()

        if resultado == QMessageBox.StandardButton.Yes:
            for linha in linhas:
                #Remover o cadastro da referente a linha
                cadastro = self.get_cadastro(linha.row())
                self.db.remover_cadastro(cadastro[0])
            
            if linhasRemovidas:
                QMessageBox.information(self, "Sucesso", f"Linhas Removidas com Sucesso: {linhasRemovidas}")

            self.atualizar_tabela()

    def atualizar_tabela(self):
        dados = self.db.ler_cadastro()
        self.cadastros = dados
        self.ui.tableWidget.setRowCount(len(dados))

        for linha, dado in enumerate(dados):
            self.ui.tableWidget.setItem(linha, 0, QTableWidgetItem(dado[1]))
            self.ui.tableWidget.setItem(linha, 1, QTableWidgetItem(dado[2]))
            self.ui.tableWidget.setItem(linha, 2, QTableWidgetItem(dado[3]))

    def cadastrar(self, nome, telefone, email):
        self.db.criar_cadastro(nome, telefone, email)
        self.atualizar_tabela()

class JanelaCadastro(QWidget):
    def __init__(self, janelaPrincipal):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.janelaPrincipal : JanelaPrincipal = janelaPrincipal
        self.cadastro = None

        self.ui.botaoOk.clicked.connect(self.aplicar)
        self.ui.botaoOk.clicked.connect(self.close)
        self.ui.editEmail.returnPressed.connect(self.aplicar)

        self.ui.editNome.setFocus()
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

    def modo_cadastro(self):
        self.setWindowTitle("Adicionar")
        self.ui.editNome.setText("")
        self.ui.editTelefone.setText("")
        self.ui.editEmail.setText("")
        self.cadastro = None
        self.show()
    
    def modo_alterar(self, cadastro):
        self.setWindowTitle("Alterar")
        self.ui.editNome.setText(cadastro[1])
        self.ui.editTelefone.setText(cadastro[2])
        self.ui.editEmail.setText(cadastro[3])
        self.cadastro = cadastro
        self.show()

    def aplicar(self):
        nome = self.ui.editNome.text()
        telefone = self.ui.editTelefone.text()
        email = self.ui.editEmail.text()

        if not nome or not telefone or not email:
            QMessageBox.warning(self, "Error", "Existem Campos em Branco")

        if self.cadastro:
            self.janelaPrincipal.alterar_cadastro(self.cadastro[0], nome, telefone, email)
        else:
            self.janelaPrincipal.cadastrar(nome, telefone, email)

        self.close()

app = QApplication([])

janela = JanelaPrincipal()
janela.show()
app.exec()