
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from os.path import isfile



class DropItem(QListWidgetItem):
    def __init__(self, text, typeWidget, icon=None, contentOption=None, *__args):
        super().__init__(*__args)
        if contentOption is not None:

            self.contentOption = contentOption["contentOption"]
        else:
            self.contentOption = "iconAndText"
        # print(contentOption, "!!!!!!!!!!!!!!")
        self.typeWidget = typeWidget
        self.setTextAlignment(Qt.AlignLeft)
        self.setText(text)



        if icon and isfile(icon):
            if self.contentOption == 'onlyIcon':
                self.setText("")
            self.setIcon(QIcon(icon))


class DropListWidget(QListWidget):
    def __init__(self, dropItems, parent, name):
        """

        :param dropItems: list(str, str)
        dropItem -> text_ClassWidget
        формат строки обязателен вначале идёт текст видимый в QListWidget
        и через разделитель < _ > тип пользовательского виджета
        :param parent:
        :param name:
        """
        super().__init__(parent)
        self.setObjectName(name)
        self.parent = parent
        self.setFont(QFont("Arial", 12))
        self.setDragEnabled(True)
        self.setFixedWidth(150)

        self.dropItems = dropItems
        self._setItems(self.dropItems)


    def _setItems(self, drop_items):
        for id, (text, type, *args) in enumerate(drop_items):

            option = args[1] if len(args)== 2 else None
            icon = args[0] if args else None
            self.insertItem(id, DropItem(text, type, icon=icon, contentOption=option))


    def mouseMoveEvent(self, e):
        mimeData = QMimeData()
        item = self.currentItem()
        mimeText = "_".join((item.text(), item.typeWidget))
        print(mimeText)
        mimeData.setText(mimeText)
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        dropAction = drag.exec_(Qt.MoveAction)
