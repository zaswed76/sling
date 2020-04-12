from PyQt5.QtCore import QFile, QIODevice, QMimeData, QPoint, Qt, QTextStream
from PyQt5.QtGui import QDrag, QPalette, QPixmap
from PyQt5.QtWidgets import QApplication, QFrame, QLabel, QWidget

# import draggabletext_rc


class DragLabel(QLabel):
    def __init__(self, text, parent):
        super(DragLabel, self).__init__(text, parent)

        self.setAutoFillBackground(True)
        self.setFrameShape(QFrame.Panel)
        self.setFrameShadow(QFrame.Raised)

    def mousePressEvent(self, event):
        hotSpot = event.pos()

        mimeData = QMimeData()
        mimeData.setText(self.text())
        mimeData.setData('application/x-hotspot',
                b'%d %d' % (hotSpot.x(), hotSpot.y()))

        pixmap = QPixmap(self.size())
        self.render(pixmap)

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setPixmap(pixmap)
        drag.setHotSpot(hotSpot)

        dropAction = drag.exec_(Qt.CopyAction | Qt.MoveAction, Qt.CopyAction)

        if dropAction == Qt.MoveAction:
            self.close()
            self.update()


class DragWidget(QWidget):
    def __init__(self, parent=None):
        super(DragWidget, self).__init__(parent)

        dictionaryFile = QFile(':/dictionary/words.txt')
        dictionaryFile.open(QIODevice.ReadOnly)

        x = 5
        y = 5

        wordLabel = DragLabel("word", self)
        wordLabel.move(x, y)
        wordLabel.show()


        newPalette = self.palette()
        newPalette.setColor(QPalette.Window, Qt.white)
        self.setPalette(newPalette)

        self.setAcceptDrops(True)
        self.setMinimumSize(400, max(200, y))
        self.setWindowTitle("Draggable Text")

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            if event.source() in self.children():
                event.setDropAction(Qt.MoveAction)
                event.accept()
            else:
                event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasText():
            mime = event.mimeData()
            pieces = mime.text().split()
            position = event.pos()
            hotSpot = QPoint()

            hotSpotPos = mime.data('application/x-hotspot').split(' ')
            if len(hotSpotPos) == 2:
               hotSpot.setX(hotSpotPos[0].toInt()[0])
               hotSpot.setY(hotSpotPos[1].toInt()[0])

            for piece in pieces:
                newLabel = DragLabel(piece, self)
                newLabel.move(position - hotSpot)
                newLabel.show()

                position += QPoint(newLabel.width(), 0)

            if event.source() in self.children():
                event.setDropAction(Qt.MoveAction)
                event.accept()
            else:
                event.acceptProposedAction()
        else:
            event.ignore()


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    window = DragWidget()
    window.show()
    sys.exit(app.exec_())