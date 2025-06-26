from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QLineEdit, QHBoxLayout, QLabel

class JanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Uma Aplicação Muito Pika")

        botao = QPushButton("Clique aqui vai, Clica clica") # Cria um botão com label "Clique aqui"
        botao.clicked.connect(self.evento_botao) # Conecta o evento de clique do botão a um método

        self.caixaTexto = QLineEdit() # Cria um campo de texto com label "Digite algo aqui"
        
        self.labelResultado = QLabel("Resultado: ")

        layoutH = QHBoxLayout() # Cria um layout horizontal
        layoutH.addWidget(QLabel("Digite um Negocio ai:"))  # Adiciona um rótulo para o campo de texto
        layoutH.addWidget(self.caixaTexto)
        layoutH.addWidget(botao)
        layoutH.addWidget(self.labelResultado)

        layoutC = QWidget() # Cria um widget para conter o layout
        layoutC.setLayout(layoutH)
        self.setCentralWidget(layoutC)

    def evento_botao(self):
        print(f"Texto Digitado: {self.caixaTexto.text()}")
        self.labelResultado.setText(f"Resultado: {self.caixaTexto.text()}")


app = QApplication([]) # Instancia de QApplication

janela = JanelaPrincipal()
janela.show() # Exibe a janela

app.exec() # Inicia o loop de eventos da aplicação
