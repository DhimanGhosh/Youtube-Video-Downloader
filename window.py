from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt6.QtGui import QIcon
from pytube import YouTube


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.icon = 'download.ico'

        # App Window
        self.setWindowIcon(QIcon(self.icon))
        self.setWindowTitle('YouTube Downloader')
        self.setGeometry(800, 450, 300, 200)  # X, Y, W, H

        # Canvas
        stylesheet = ('''
            QWidget {
                font-size: 18px;
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
        button = QPushButton('Download')

        layout.addWidget(label)
        layout.addWidget(self.inputField)
        layout.addWidget(button)

        button.clicked.connect(self.start_download)

    def start_download(self):
        url = self.inputField.text()
        yt = YouTube(url)
        yt.streams.get_highest_resolution().download()
