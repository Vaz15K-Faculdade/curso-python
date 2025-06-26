from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QLineEdit, QHBoxLayout

class JanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        botao = QPushButton("Clique aqui") # Cria um botão com label "Clique aqui"
        texto = QLineEdit("Digite algo aqui") # Cria um campo de texto com label "Digite algo aqui"
        # Esse texto aparece como escrito
        
        layout_h = QHBoxLayout() # Cria um layout horizontal
        layout_h.addWidget(botao)
        layout_h.addWidget(texto)

        layout_c = QWidget() # Cria um widget para conter o layout
        layout_c.setLayout(layout_h)
        self.setCentralWidget(layout_c)


app = QApplication([]) # Instancia de QApplication

janela = JanelaPrincipal()
janela.show() # Exibe a janela

app.exec() # Inicia o loop de eventos da aplicação
