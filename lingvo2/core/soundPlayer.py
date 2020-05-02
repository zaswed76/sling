import os
import sys

from PyQt5 import QtCore, QtWidgets, QtMultimedia




class Widget(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()






if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    main = Widget()
    filename = 'brother.mp3'
    fullpath = QtCore.QDir.current().absoluteFilePath(filename)
    main.play(fullpath)
    main.show()
    sys.exit(app.exec_())

# import sys
# from PyQt5 import QtCore, QtWidgets, QtMultimedia
# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     filename = 'brother.mp3'
#     fullpath = QtCore.QDir.current().absoluteFilePath(filename)
#     url = QtCore.QUrl.fromLocalFile(fullpath)
#     content = QtMultimedia.QMediaContent(url)
#     player = QtMultimedia.QMediaPlayer()
#     player.setMedia(content)
#     player.play()
#     sys.exit(app.exec_())