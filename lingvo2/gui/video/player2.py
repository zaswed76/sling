from PyQt5.QtCore import QDir, QSize, QSizeF, Qt, QUrl, QPointF
from PyQt5.QtGui import QTransform
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QGraphicsVideoItem
from PyQt5.QtWidgets import (QApplication, QFileDialog, QGraphicsScene,
        QGraphicsView, QHBoxLayout, QPushButton, QSlider, QStyle, QVBoxLayout,
        QWidget)



class VideoItem(QGraphicsVideoItem):
    def __init__(self):
        super().__init__()







import paths
class VideoPlayer(QWidget):

    def __init__(self, cfg, playlist, main, parent=None):
        super(VideoPlayer, self).__init__(parent)

        self.main = main
        self.playlist = playlist
        self.cfg = cfg
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        self.videoItem = VideoItem()
        self.videoItem.setAspectRatioMode(Qt.KeepAspectRatio)

        width = self.cfg["ui"]["viewCardWidth"]
        height = self.cfg["ui"]["viewCardHeight"]



        scene = QGraphicsScene(self)
        # scene.setSceneRect(0, 0, 838, 610)
        self.graphicsView = QGraphicsView(scene)
        # self.setFixedSize(960, 598)
        # self.graphicsView.mapToScene(28, 28)
        print(self.graphicsView.mapToScene(width, height))
        self.videoItem.setSize(QSizeF(width, height))

        scene.addItem(self.videoItem)

        openButton = QPushButton("Open...")
        openButton.clicked.connect(self.openFile)

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(openButton)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.graphicsView)
        layout.addLayout(controlLayout)

        self.setLayout(layout)

        self.mediaPlayer.setVideoOutput(self.videoItem)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)

    # def sizeHint(self):
    #     return QSize(800, 600)

    def setFile(self, fileName):
        self.mediaPlayer.setMedia(
            QMediaContent(QUrl.fromLocalFile(fileName)))

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                                                  str(paths.DICTIONARIES))
        if fileName != '':
            self.setFile(fileName)
            self.playButton.setEnabled(True)

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)




if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)

    player = VideoPlayer(None, "", None)
    player.show()

    sys.exit(app.exec_())