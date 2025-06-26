# -----------------------------------------------
# pip install pyqt6
# arquivo caixa.py
# https://dontpad.com/cyber0406
# 10.0.0.49:8000
# -----------------------------------------------
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QColor, QPalette

class CaixaCor(QWidget):
    def __init__(self, color, min_h = None, min_w = None):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)

        if min_h:
            self.setMinimumHeight(min_h)
        
        if min_w:
            self.setMinimumWidth(min_w)