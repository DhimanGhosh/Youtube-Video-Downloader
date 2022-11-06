from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QFileDialog, QHBoxLayout
from PyQt6.QtGui import QIcon
from pytube import YouTube
from glob import glob
import subprocess
import os
import shutil
import urllib.request
import json
import urllib


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.icon = 'download.ico'

        # App Window
        self.setWindowIcon(QIcon(self.icon))
        self.setWindowTitle('YouTube Downloader')
        self.setGeometry(800, 450, 350, 250)  # X, Y, W, H
        self.setFixedWidth(350)
        self.setFixedHeight(250)

        # Canvas
        stylesheet = ('''
            QWidget {
                font-size: 14px;
            }
        ''')
        self.setStyleSheet(stylesheet)

        # Layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Widgets
        # URL
        label = QLabel('Youtube video URL')
        self.url = QLineEdit()

        # Save To (Horizontal Layout)
        save_to_label = QLabel('Save File To...')
        save_to_layout = QHBoxLayout()
        self.save_to_path = QLineEdit()
        save_to_btn = QPushButton('Browse')
        save_to_layout.addWidget(self.save_to_path, )
        save_to_layout.addWidget(save_to_btn)

        # Download
        download_button = QPushButton('Download Video')
        download_mp3_button = QPushButton('Download Audio')

        # Status
        self.status_label = QLabel()

        layout.addWidget(label)
        layout.addWidget(self.url)
        layout.addWidget(save_to_label)
        layout.addLayout(save_to_layout)
        layout.addWidget(download_button)
        layout.addWidget(download_mp3_button)
        layout.addWidget(self.status_label)

        download_button.clicked.connect(self.__start_download)
        download_mp3_button.clicked.connect(self.__start_download_mp3)
        save_to_btn.clicked.connect(self.__save_to_dialog)

    def __start_download(self):
        url = self.url.text()
        yt = YouTube(url)
        self.__display_status('Downloading video... Please Wait!')
        yt.streams.get_highest_resolution().download()
        downloaded_file = glob('*.mp4')[0]
        if downloaded_file:
            self.__move_to(downloaded_file=downloaded_file, media_extension='.mp4')
            self.__display_status('Video Download completed!')
        else:
            self.__display_status('Error in Video Download!')

    def __start_download_mp3(self):
        url = self.url.text()
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
        downloaded_file = glob('*.mp3')[0]
        if downloaded_file:
            self.__move_to(downloaded_file=downloaded_file, media_extension='.mp3')
            self.__display_status('Audio Download completed!')
        else:
            self.__display_status('Error in Audio Download!')

    def __save_to_dialog(self):
        url = self.url.text()
        if url:
            title = self.__get_video_title(url)
            title = title.replace('|', ', ')
        else:
            title = 'Sample'
        downloads_directory = f"C:\\Users\\{os.environ.get('USERNAME')}\\Downloads\\{title}"
        downloadable_formats = "Audio (*.mp3)\nVideo (*.mp4)"
        path, _ = QFileDialog.getSaveFileName(parent=self, caption='Save File', directory=downloads_directory, filter=downloadable_formats, initialFilter='File')
        self.save_to_path.setText(path.replace('/', os.sep))

    def __display_status(self, msg: str):
        self.status_label.setText(msg)

    def __move_to(self, downloaded_file, media_extension='.mp4'):
        move_to_path = self.save_to_path.text()
        if move_to_path:
            if '.' not in move_to_path.split(os.sep)[-1]:  # if file extension not specified
                move_to_path += media_extension
            if move_to_path.split(os.sep)[-1].split('.')[-1] != media_extension[1:]:  # if incorrect file extension specified
                move_to_path = os.sep.join(move_to_path.split(os.sep)[:-1]) + os.sep + move_to_path.split(os.sep)[-1].split('.')[0] + media_extension
            shutil.copy(downloaded_file, move_to_path)
            os.remove(downloaded_file)

    def __get_video_title(self, url):
        params = {"format": "json", "url": url}
        video_url = "https://www.youtube.com/oembed"
        query_string = urllib.parse.urlencode(params)
        video_url += "?" + query_string

        with urllib.request.urlopen(video_url) as response:
            response_text = response.read()
            data = json.loads(response_text.decode())
            return data['title']
