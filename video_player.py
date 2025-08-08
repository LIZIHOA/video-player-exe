
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout,
    QFileDialog, QSlider, QStyle, QLabel, QHBoxLayout
)
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl


class VideoPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("本地视频播放器")
        self.setGeometry(200, 200, 800, 600)

        # 媒体播放器
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        # 视频显示组件
        videowidget = QVideoWidget()

        # 打开文件按钮
        openBtn = QPushButton('打开文件')
        openBtn.clicked.connect(self.open_file)

        # 播放按钮
        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)

        # 进度条
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.set_position)

        # 音量控制
        volumeLabel = QLabel('音量:')
        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setValue(50)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.sliderMoved.connect(self.mediaPlayer.setVolume)

        # 布局
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(openBtn)
        controlLayout.addWidget(self.playBtn)
        controlLayout.addWidget(self.slider)
        controlLayout.addWidget(volumeLabel)
        controlLayout.addWidget(self.volumeSlider)

        layout = QVBoxLayout()
        layout.addWidget(videowidget)
        layout.addLayout(controlLayout)

        self.setLayout(layout)

        self.mediaPlayer.setVideoOutput(videowidget)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "打开视频")
        if filename != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.playBtn.setEnabled(True)

    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        else:
            self.mediaPlayer.play()
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))

    def position_changed(self, position):
        self.slider.setValue(position)

    def duration_changed(self, duration):
        self.slider.setRange(0, duration)

    def set_position(self, position):
        self.mediaPlayer.setPosition(position)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec_())
