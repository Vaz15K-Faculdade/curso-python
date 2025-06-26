from PyQt6.QtWidgets import *
from caixa import CaixaCor

class JanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(512, 340)

        caixa = CaixaCor("#328a4f")
        caixa2 = CaixaCor("#96084C")
        caixa3 = CaixaCor("#a4c417")
        caixa4 = CaixaCor("#170BBE")

        layoutV = QVBoxLayout()
        layoutV.addWidget(caixa, 9)
        layoutV.addWidget(caixa2, 5)
        layoutV.addWidget(caixa3, 5)
        layoutV.addWidget(caixa4, 1)

        componenteCentral = QWidget()
        componenteCentral.setLayout(layoutV)
        self.setCentralWidget(componenteCentral)

app = QApplication([])
janela = JanelaPrincipal()
janela.show()
app.exec()