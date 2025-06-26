from PyQt6.QtWidgets import *
from caixa import CaixaCor

class JanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(240, 360)

        expandir = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        caixaResultado = QListWidget()
        caixaInput = QLineEdit()

        caixaIgual = QPushButton("=")
        teclaMa = QPushButton("+")
        teclaMe = QPushButton("-")
        teclaMu = QPushButton("*")
        teclaDi = QPushButton("/")
        teclaPo = QPushButton("%") 
        teclaC = QPushButton("C") 

        tecla1 = QPushButton("1")
        tecla2 = QPushButton("2")
        tecla3 = QPushButton("3")
        tecla4 = QPushButton("4")
        tecla5 = QPushButton("5")
        tecla6 = QPushButton("6")
        tecla7 = QPushButton("7")
        tecla8 = QPushButton("8")
        tecla9 = QPushButton("9")
        tecla0 = QPushButton("0")
        teclaVi = QPushButton(",")
        teclaMM = QPushButton("+/-")

        layoutG = QGridLayout()
        layoutG.addWidget(caixaResultado, 1, 1, 1, 4)
        layoutG.addWidget(caixaInput, 3, 1, 1, 4)

        layoutG.addWidget(teclaMa, 4, 1)
        layoutG.addWidget(teclaMe, 4, 2)
        layoutG.addWidget(teclaMu, 4, 3)
        layoutG.addWidget(teclaDi, 4, 4)
        layoutG.addWidget(teclaPo, 5, 4)
        layoutG.addWidget(teclaC, 6, 4)

        layoutG.addWidget(tecla7, 5, 1)
        layoutG.addWidget(tecla4, 6, 1)
        layoutG.addWidget(tecla1, 7, 1)
        
        layoutG.addWidget(tecla8, 5, 2)
        layoutG.addWidget(tecla5, 6, 2)
        layoutG.addWidget(tecla2, 7, 2)

        layoutG.addWidget(tecla9, 5, 3)
        layoutG.addWidget(tecla6, 6, 3)
        layoutG.addWidget(tecla3, 7, 3)

        layoutG.addWidget(teclaVi, 8, 1)
        layoutG.addWidget(tecla0, 8, 2)
        layoutG.addWidget(teclaMM, 8, 3)

        layoutG.addWidget(caixaIgual, 7, 4, 2, 1)

        componenteCentral = QWidget()
        componenteCentral.setLayout(layoutG)
        self.setCentralWidget(componenteCentral)

        caixaResultado.setSizePolicy(expandir)
        caixaInput.setSizePolicy(expandir)

        for botao in self.findChildren(QPushButton):
            botao.setSizePolicy(expandir)

        self.setStyleSheet("""
            QPushButton {
                border-radius: 10px;
                color: white;
                background-color: #808080;
                font-size: 24px;
            }
            QLineEdit {
                font-size: 24px;
            }
            QListWidget {
                font-size: 18px;
            }
        """)
        
        caixaInput.returnPressed.connect(self.calcular)
        caixaIgual.clicked.connect(self.calcular)
        caixaResultado.itemDoubleClicked.connect(self.return_item)

        teclaC.clicked.connect(self.caixaInput.clear)

        self.caixaInput = caixaInput
        self.caixaResultado = caixaResultado

    def calcular(self):
        expressao = self.caixaInput.text()
        try:
            resultado = eval(expressao)
        except:
            resultado = "Erro"
        self.caixaResultado.addItem(f"{expressao} = {resultado}")
        self.caixaResultado.scrollToBottom()
        self.caixaInput.setText(f"{resultado}")

    def return_item(self):
        item = self.caixaResultado.currentItem()
        if item:
            texto = item.text()
            self.caixaInput.setText(texto.split(" = ")[0])

app = QApplication([])
janela = JanelaPrincipal()
janela.show()
app.exec()