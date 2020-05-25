#!/usr/bin/env python3

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from gui.video.player2 import VideoPlayer

from gui.custom.customwidgets import *







class Video(QFrame):
    def __init__(self, main, objectName=None, config=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.main = main
        self.cfg = config
        self.setObjectName(objectName)
        self.player = VideoPlayer(self.cfg, "", self.main, None)
        self.box = BoxLayout(QBoxLayout.TopToBottom, self)
        self.box.addWidget(self.player)

    def setFile(self, file):
        self.player.setFile(file)
        self.player.playButton.setEnabled(True)

    def play(self):
        self.player.play()

    def pause(self):
        self.player.mediaPlayer.pause()

    def setSizeVideo(self, w, h):
        qsizef = QSizeF(w, h)
        self.player.videoItem.setSize(qsizef)
        self.player.graphicsView.setFixedSize(w+2, h+2)
        # self.player.graphicsView.setS





if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet(open('./etc/{0}.qss'.format('style'), "r").read())
    main = Video()
    main.show()
    sys.exit(app.exec_())