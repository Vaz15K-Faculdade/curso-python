from PyQt6.QtWidgets import *
from caixa import CaixaCor

class JanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(512, 340)

        caixa = CaixaCor("#328a4f")

        fundoBandeira = QHBoxLayout()
        fundoBandeira.addWidget(caixa)

        componenteCentral = QWidget()
        componenteCentral.setLayout(fundoBandeira)
        self.setCentralWidget(componenteCentral)

app = QApplication([])
janela = JanelaPrincipal()
janela.show()
app.exec()