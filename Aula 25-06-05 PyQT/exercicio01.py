from PyQt6.QtWidgets import *
from caixa import CaixaCor

class JanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(512, 340)
        
        caixa = CaixaCor("#025BFF")
        caixa2 = CaixaCor("#044720")
        caixa3 = CaixaCor("#486148")
        layoutH = QHBoxLayout()
        layoutH.addWidget(caixa2, 3)
        layoutH.addWidget(caixa3, 2)
        layoutV = QVBoxLayout()
        layoutV.addWidget(caixa, 8)
        layoutV.addLayout(layoutH, 2)
        
        caixa4 = CaixaCor("#214624")
        caixa5 = CaixaCor("#960404")
        caixa6 = CaixaCor("#C8FF00")
        caixa7 = CaixaCor("#57074C")
        layoutH2 = QHBoxLayout()
        layoutH2.addWidget(caixa4, 4)
        layoutH2.addWidget(caixa5, 4)
        layoutH2.addWidget(caixa6, 3)
        layoutV2 = QVBoxLayout()
        layoutV2.addLayout(layoutH2, 1)
        layoutV2.addWidget(caixa7, 9)

        layout = QHBoxLayout()
        layout.addLayout(layoutV, 5)
        layout.addLayout(layoutV2, 11)

        componenteCentral = QWidget()
        componenteCentral.setLayout(layout)
        self.setCentralWidget(componenteCentral)

app = QApplication([])
janela = JanelaPrincipal()
janela.show()
app.exec()