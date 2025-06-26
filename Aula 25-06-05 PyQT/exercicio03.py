from PyQt6.QtWidgets import *
from caixa import CaixaCor

class JanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(512, 340)

        caixa1 = CaixaCor("#008ecf")
        caixa2 = CaixaCor("#07570D")
        caixa3 = CaixaCor("#334735")

        caixa4 = CaixaCor("#17FF17")
        caixa5 = CaixaCor("#640606")
        caixa6 = CaixaCor("#5E810B")
        caixa7 = CaixaCor("#E91196")

        layoutG = QGridLayout()
        layoutG.addWidget(caixa1, 1, 1, 8, 5)
        layoutG.addWidget(caixa2, 9, 1, 2, 3)
        layoutG.addWidget(caixa3, 9, 4, 2, 2)

        layoutG.addWidget(caixa4, 1, 6, 1, 4)
        layoutG.addWidget(caixa5, 1, 10, 1, 4)
        layoutG.addWidget(caixa6, 1, 14, 1, 3)

        layoutG.addWidget(caixa7, 2, 6, 9, 11)

        componenteCentral = QWidget()
        componenteCentral.setLayout(layoutG)
        self.setCentralWidget(componenteCentral)

app = QApplication([])
janela = JanelaPrincipal()
janela.show()
app.exec()