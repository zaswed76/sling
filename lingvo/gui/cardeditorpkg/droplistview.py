
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from os.path import isfile



class DropItem(QListWidgetItem):
    def __init__(self, text, typeWidget, icon=None, contentOption="iconAndText", *__args):
        """

        :param text: str
        :param typeWidget: usertypeWidget
        :param icon: str path
        :param contentOption: onlyIcon or iconAndText or None
        :param __args:
        """
        super().__init__(*__args)
        self.contentOption = contentOption



        self.typeWidget = typeWidget
        self.setTextAlignment(Qt.AlignLeft)
        self.setText(text)

        if icon and isfile(icon):
            if self.contentOption == 'onlyIcon':
                self.setText("")
            self.setIcon(QIcon(icon))


class DropListWidget(QListWidget):
    def __init__(self, dropItemsTypeList, parent, name):
        """
        :param dropItems: list(dropItem: list, dropItem: list ...)
        dropItem example1 -> [ExampleText, ClassWidget]
        dropItem example2 -> [IconAndText, ClassWidget, ./resources/icons/base/icon_gift_alt.png]
        dropItem example3 -> [OnlyIcon, ClassWidget, ./resources/icons/base/icon_gift_alt.png, onlyIcon]
        :param parent: QWidget
        :param name: str ObjectName
        """
        super().__init__(parent)
        self.setObjectName(name)
        self.parent = parent
        self.setFont(QFont("Arial", 12))
        self.setDragEnabled(True)
        self.setFixedWidth(150)

        self.dropItemsTypeList = dropItemsTypeList
        self._setItems(self.dropItemsTypeList)


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
