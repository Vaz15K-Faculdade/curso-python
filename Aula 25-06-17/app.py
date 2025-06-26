from PySide6.QtWidgets import *
from PySide6.QtGui import *
from calculadoraUI import Ui_MainWindow

class JanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.lista_contas = self.ui.listWidget
        self.expressao = self.ui.lineEdit

        self.ui.listWidget.itemDoubleClicked.connect(self.retornar_expr)
        self.ui.lineEdit.returnPressed.connect(self.calcular)

        self.ui.botaoC.clicked.connect(self.apagar)
        self.ui.butaoIgual.clicked.connect(self.calcular)

        for botao in self.findChildren(QPushButton):
            if botao != self.ui.butaoIgual and botao != self.ui.botaoC:
                botao.clicked.connect(self.evento_botoes)
    
    def evento_botoes(self):
        botao : QPushButton = self.sender()
        label = botao.text()

        operador = ''
        match label:
            case '÷':
                operador = '/'
            case '×':
                operador = '*'
            case '%':
                operador = '/100'
            case '+/-':
                operador = '*-1'
            case ',':
                operador = '.'
            case _:
                operador = label

        expr = self.expressao.text()
        self.expressao.setText(expr + operador)        

        if label == '+/-' or label == '%':
            self.calcular()
        
        self.expressao.setFocus()

    def apagar(self):
        self.expressao.clear()
        self.expressao.setFocus()

    def retornar_expr(self):
        item = self.lista_contas.currentItem()
        if item:
            texto = item.text()
            self.expressao.setText(texto.split(' = ')[-1])
            self.expressao.setFocus()

    def calcular(self):
        expr = self.expressao.text()
        
        color_res = QColor("#9f3c3c")
        try:
            resultado = eval(expr)
            color_res = QColor("#3FC285")
        except ZeroDivisionError:
            resultado = "DivisÃ£o por zero"
        except NameError:
            resultado = "VariÃ¡vel nÃ£o definida"
        except SyntaxError:
            resultado = "Erro de sintaxe"
        except:
            resultado = "Erro"

        item_expr = QListWidgetItem(f'{expr}')
        item_expr.setTextAlignment(Qt.AlignmentFlag.AlignRight)
        self.lista_contas.addItem(item_expr)

        item_res = QListWidgetItem(f' = {resultado}')
        item_res.setTextAlignment(Qt.AlignmentFlag.AlignRight)
        item_res.setForeground(color_res)
        self.lista_contas.addItem(item_res)

        self.lista_contas.scrollToBottom()
        self.expressao.setText(f'{resultado}')
        self.expressao.setFocus()

app = QApplication([])
janela = JanelaPrincipal()
janela.show()
app.exec()