
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class Style:
    Align = dict(left=Qt.AlignLeft, right=Qt.AlignRight, center=Qt.AlignCenter)
    def __init__(self, font_name="Tahoma", font_size=16, italic=False,
                 text_color="darkgrey", align="center", content_marging=(0, 0, 0, 0)):

        self.contentMarging = content_marging
        self.align = self.Align[align]
        self.textColor = text_color
        self.italic = italic
        self.fontSize = font_size
        self.fontName = font_name
        self.font = QFont(self.fontName, self.fontSize, self.italic)


style = Style()
style.fontName = "Helvetica"

def setStyleContent(self, text, style):
    self.setText("this is an example in english")
    self.setFont(QFont("Helvetica", 14, italic=True))
    self.setStyleSheet("QLabel { color: #144676 }")
    self.setAlignment(Qt.AlignLeft)
    self.setContentsMargins(70, 10, 0, 0)