from PyQt6.QtWidgets import *
from caixa import CaixaCor

class JanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(512, 340)

        caixa = CaixaCor("#74042F")
        caixa2 = CaixaCor("#96088A")
        caixa3 = CaixaCor("#008ecf")
        caixa4 = CaixaCor("#07570D")

        layoutV = QVBoxLayout()
        layoutV.addWidget(caixa3, 8)
        layoutV.addWidget(caixa4, 2)

        layoutH = QHBoxLayout()
        layoutH.addWidget(caixa, 2)
        layoutH.addWidget(caixa2, 10)
        layoutH.addLayout(layoutV, 4)

        componenteCentral = QWidget()
        componenteCentral.setLayout(layoutH)
        self.setCentralWidget(componenteCentral)

app = QApplication([])
janela = JanelaPrincipal()
janela.show()
app.exec()