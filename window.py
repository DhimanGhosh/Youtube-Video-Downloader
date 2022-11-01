from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt6.QtGui import QIcon
from pytube import YouTube
from glob import glob
import subprocess
import os


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.icon = 'download.ico'

        # App Window
        self.setWindowIcon(QIcon(self.icon))
        self.setWindowTitle('YouTube Downloader')
        self.setGeometry(800, 450, 300, 200)  # X, Y, W, H
        self.setFixedWidth(300)
        self.setFixedHeight(200)

        # Canvas
        stylesheet = ('''
            QWidget {
                font-size: 12px;
            }

            QPushButton {
                font-size: 20px;
            }
        ''')
        self.setStyleSheet(stylesheet)

        # Layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # widgets
        label = QLabel('Youtube video URL')
        self.inputField = QLineEdit()
        download_button = QPushButton('Download')
        download_mp3_button = QPushButton('Download MP3')
        self.status_label = QLabel()

        layout.addWidget(label)
        layout.addWidget(self.inputField)
        layout.addWidget(download_button)
        layout.addWidget(download_mp3_button)
        layout.addWidget(self.status_label)

        download_button.clicked.connect(self.start_download)
        download_mp3_button.clicked.connect(self.start_download_mp3)

    def start_download(self):
        url = self.inputField.text()
        yt = YouTube(url)
        self.__display_status('Downloading video... Please Wait!')
        yt.streams.get_highest_resolution().download()
        if glob('*.mp4'):
            self.__display_status('Video Download completed!')
        else:
            self.__display_status('Error in Video Download!')

    def start_download_mp3(self):
        url = self.inputField.text()
        self.__display_status('Downloading Audio... Please Wait!')
        yt = YouTube(url)
        yt.streams.get_highest_resolution().download()
        video_file = glob('*.mp4')[0]
        video_file_rename = 'video.'+video_file.split('.')[-1]
        audio_file = 'audio.mp3'
        os.rename(video_file, video_file_rename)
        subprocess.call(f'ffmpeg -i {video_file_rename} -vn {audio_file}')
        os.remove(video_file_rename)
        os.rename(audio_file, video_file.split('.')[0] + '.mp3')
        if glob('*.mp3'):
            self.__display_status('Audio Download completed!')
        else:
            self.__display_status('Error in Audio Download!')

    def __display_status(self, msg: str):
        self.status_label.setText(msg)
