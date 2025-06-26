from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget

class JanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        botao = QPushButton("Clique aqui") # Cria um botão com label "Clique aqui"
        self.setCentralWidget(botao) # Define o botao como componente central da janela


app = QApplication([]) # Instancia de QApplication

janela = JanelaPrincipal()
janela.show() # Exibe a janela

app.exec() # Inicia o loop de eventos da aplicação
