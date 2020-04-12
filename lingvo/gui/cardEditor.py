

#!/usr/bin/env python3

import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import *

def qt_message_handler(mode, context, message):
    if mode == QtInfoMsg:
        mode = 'INFO'
    elif mode == QtWarningMsg:
        mode = 'WARNING'
    elif mode == QtCriticalMsg:
        mode = 'CRITICAL'
    elif mode == QtFatalMsg:
        mode = 'FATAL'
    else:
        mode = 'DEBUG'
    print('qt_message_handler: line: %d, func: %s(), file: %s' % (
          context.line, context.function, context.file))
    print('  %s: %s\n' % (mode, message))

qInstallMessageHandler(qt_message_handler)


class TestListView(QtWidgets.QListWidget):

    def __init__(self, parent):
        super(TestListView, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setIconSize(QtCore.QSize(100, 100))
        # self.itemClicked.connect(self.on_item_clicked)
        self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)


    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.acceptProposedAction()
        else:
            super(TestListView, self).dragEnterEvent(event)

    def dragMoveEvent(self, event):
        super(TestListView, self).dragMoveEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
            self.emit(QtCore.SIGNAL("dropped"), links)
            event.acceptProposedAction()
        else:
            super(TestListView,self).dropEvent(event)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # app.setStyleSheet(open('./etc/{0}.qss'.format('style'), "r").read())
    main = TestListView(None)
    main.show()
    sys.exit(app.exec_())