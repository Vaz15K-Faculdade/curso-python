from PyQt6.QtWidgets import *
from caixa import CaixaCor

class JanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(512, 340)

        caixa1 = CaixaCor("#FF5733")
        caixa2 = CaixaCor("#33FF57")
        caixa3 = CaixaCor("#3357FF")
        caixa4 = CaixaCor("#F1C40F")
        caixa5 = CaixaCor("#9B59B6")
        caixa6 = CaixaCor("#E67E22")
        caixa7 = CaixaCor("#1ABC9C")
        caixa8 = CaixaCor("#E74C3C")
        caixa9 = CaixaCor("#34495E")

        layoutG = QGridLayout()
        layoutG.addWidget(caixa1, 1, 1, 1, 2)
        layoutG.addWidget(caixa2, 1, 3, 1, 2)
        layoutG.addWidget(caixa3, 2, 1, 2, 1)
        layoutG.addWidget(caixa4, 2, 2, 2, 3)

        componenteCentral = QWidget()
        componenteCentral.setLayout(layoutG)
        self.setCentralWidget(componenteCentral)

app = QApplication([])
janela = JanelaPrincipal()
janela.show()
app.exec()