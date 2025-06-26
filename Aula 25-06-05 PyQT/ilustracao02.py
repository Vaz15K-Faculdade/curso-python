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

        layoutH = QHBoxLayout()
        layoutH.addWidget(caixa, 4)
        layoutH.addWidget(caixa2, 5)
        layoutH.addWidget(caixa3, 3)
        layoutH.addWidget(caixa4, 8)

        componenteCentral = QWidget()
        componenteCentral.setLayout(layoutH)
        self.setCentralWidget(componenteCentral)

app = QApplication([])
janela = JanelaPrincipal()
janela.show()
app.exec()