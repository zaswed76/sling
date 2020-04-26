
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from gui.custom.abccard import AbcViewCard
#
# class ViewCard(QFrame):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#         self.setFixedSize(730, 730)
#         self.setStyleSheet("background-color: white")
#         self.box = QHBoxLayout(self)
#         self.card = Card()
#         self.box.addWidget(self.card)



class ViewCard(AbcViewCard):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedSize(790, 788)
        self.setStyleSheet("background-color: lightgrey")
        self.setToolTip("DropLayout")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet(open('./etc/{0}.qss'.format('style'), "r").read())
    main = ViewCard()
    main.show()
    sys.exit(app.exec_())