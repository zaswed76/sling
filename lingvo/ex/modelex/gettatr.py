
import sys
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QMainWindow, QApplication

import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
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
# базовый класс для всех объектов модуля
class AnyObjects(QObject):
    # создаем свой сигнал
    own_signal = pyqtSignal()

# создаем главное окно
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.set_params()

    # метод, который срабатывает при нажатии на окно
    def mousePressEvent(self, event):
        # генерируем сигнал
        self.ao.own_signal.emit()
        self.close()

    def set_params(self):
        self.ao = AnyObjects()
        # обработчик сигнала, связанного с объектом
        self.ao.own_signal.connect(self.on_clicked)
        # параметры главного окна
        self.setGeometry(900, 300, 290, 150)
        self.setWindowTitle('Пример работы самописного сигнала')
        self.show()

    def on_clicked(self):
        print('Тут сообщение')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec_())