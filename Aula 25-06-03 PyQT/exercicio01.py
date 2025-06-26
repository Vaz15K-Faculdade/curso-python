from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QLineEdit, QHBoxLayout, QLabel

class JanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Calculadora de IMC")

        self.caixaPeso = QLineEdit()
        self.caixaAltura = QLineEdit()
        self.botaoCalculo = QPushButton("Calcular IMC")
        self.botaoCalculo.clicked.connect(self.calcular_imc)
        self.labelResultado = QLabel("Resultado: ")

        layoutH = QHBoxLayout()
        layoutH.addWidget(QLabel("Peso"))
        layoutH.addWidget(self.caixaPeso)
        layoutH.addWidget(QLabel("Altura"))
        layoutH.addWidget(self.caixaAltura)
        layoutH.addWidget(self.botaoCalculo)
        layoutH.addWidget(self.labelResultado)

        layoutC = QWidget()
        layoutC.setLayout(layoutH)
        self.setCentralWidget(layoutC)

    def calcular_imc(self):
        peso = float(self.caixaPeso.text())
        altura = float(self.caixaAltura.text())
        self.labelResultado.setText(f"IMC = {peso / (altura**2)}")

app = QApplication([])

janela = JanelaPrincipal()
janela.show()

app.exec()