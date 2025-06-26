from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

app = QApplication([]) # Instancia de QApplication

janela = QMainWindow() # Instancia de QMainWindow

botao = QPushButton("Clique aqui") # Cria um botão com label "Clique aqui"
janela.setCentralWidget(botao) # Define o botao como componente central da janela

janela.showMaximized() # Exibe a janela maximizada
janela.show() # Exibe a janela

app.exec() # Inicia o loop de eventos da aplicação