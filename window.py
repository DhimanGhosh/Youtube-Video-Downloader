from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QHBoxLayout,
    QFileDialog
)
from PyQt6.QtGui import (
    QIcon
)
from glob import glob
import os
from config import widgets, window
from downloader import download, video


class Window(QWidget):

    # region constants
    X_VALUE = 800
    Y_VALUE = 450
    WIDTH = 350
    HEIGHT = 250
    APP_LABEL = 'YouTube Downloader'
    URL_LABEL = 'Youtube video URL'
    SAVE_TO_LABEL = 'Save File To...'
    BROWSE_LABEL = 'Browse'
    DOWNLOAD_VIDEO_LABEL = 'Download Video'
    DOWNLOAD_AUDIO_LABEL = 'Download Audio'
    STYLESHEET_FILE = 'stylesheet.css'
    APP_ICON = 'download.ico'
    # endregion constants

    # region colors
    RESET = 'white'
    SUCCESS = 'green'
    WARNING = 'yellow'
    ERROR = 'red'
    # endregion colors

    def __init__(self):
        super().__init__()

        # region App Window
        self.setWindowIcon(QIcon(Window.APP_ICON))
        self.setWindowTitle(Window.APP_LABEL)
        self.setGeometry(Window.X_VALUE, Window.Y_VALUE, Window.WIDTH, Window.HEIGHT)
        self.setFixedWidth(Window.WIDTH)
        self.setFixedHeight(Window.HEIGHT)
        # endregion App Window

        # region Canvas
        with open(Window.STYLESHEET_FILE, 'r') as f:
            self.setStyleSheet(f.read())
        # endregion Canvas

        # region Layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        # endregion Layout

        # region Widgets
        # region URL
        url_label = QLabel(Window.URL_LABEL)
        self.__url = QLineEdit()
        # endregion URL

        # region Save To (Horizontal Layout)
        self.__save_to_label = QLabel(Window.SAVE_TO_LABEL)
        self.__save_to_layout = QHBoxLayout()
        self.__save_to_path = QLineEdit()
        self.__save_to_browse_button = QPushButton(Window.BROWSE_LABEL)
        widgets.change_pointer_to_hand(self.__save_to_browse_button)
        self.__save_to_layout.addWidget(self.__save_to_path, )
        self.__save_to_layout.addWidget(self.__save_to_browse_button)
        # endregion Save To (Horizontal Layout)

        # region Buttons
        self.__download_video_button = QPushButton(Window.DOWNLOAD_VIDEO_LABEL)
        widgets.change_pointer_to_hand(self.__download_video_button)
        self.__download_audio_button = QPushButton(Window.DOWNLOAD_AUDIO_LABEL)
        widgets.change_pointer_to_hand(self.__download_audio_button)
        # endregion Buttons

        # Download Progress Bar
        # self.__progress_bar = ProgressBar()

        # region Status
        self.__status_label = QLabel()
        # endregion Status
        # endregion Widgets

        # region Add widgets to layout
        layout.addWidget(url_label)
        layout.addWidget(self.__url)
        layout.addWidget(self.__save_to_label)
        layout.addLayout(self.__save_to_layout)
        layout.addWidget(self.__download_video_button)
        layout.addWidget(self.__download_audio_button)
        # layout.addWidget(self.__progress_bar)
        layout.addWidget(self.__status_label)
        # endregion Add widgets to layout

        # region Bind buttons to functions
        self.__save_to_browse_button.clicked.connect(self.__save_to_dialog)
        self.__download_video_button.clicked.connect(self.__start_download_video)
        self.__download_audio_button.clicked.connect(self.__start_download_audio)
        # endregion Bind buttons to functions

    def __save_to_dialog(self):
        url = self.__url.text()
        if url:
            title = video.get_video_title(url)
            title = title.replace('|', ', ')
        else:
            title = 'Sample'
        downloads_directory = f"C:\\Users\\{os.environ.get('USERNAME')}\\Downloads\\{title}"
        downloadable_formats = "Audio (*.mp3)\nVideo (*.mp4)"
        path, _ = QFileDialog.getSaveFileName(
            parent=self,
            caption='Save File',
            directory=downloads_directory,
            filter=downloadable_formats,
            initialFilter='File'
        )
        self.__save_to_path.setText(path.replace('/', os.sep))

    def __start_download_video(self):
        url = self.__url.text()
        window.display_status(status_label=self.__status_label, msg='Downloading video... Please Wait!', wait_time=5)
        download.download_video(url)
        downloaded_file = glob('*.mp4')[0]
        if downloaded_file:
            video.move_to(save_to_path=self.__save_to_path, downloaded_file=downloaded_file, media_extension='.mp4')
            window.display_status(status_label=self.__status_label, msg='Video Download completed!')
        else:
            window.display_status(status_label=self.__status_label, msg='Error in Video Download!')

    def __start_download_audio(self):
        url = self.__url.text()
        window.display_status(status_label=self.__status_label, msg='Downloading audio... Please Wait!', wait_time=5)
        download.download_audio(url)
        downloaded_file = glob('*.mp3')[0]
        if downloaded_file:
            video.move_to(save_to_path=self.__save_to_path, downloaded_file=downloaded_file, media_extension='.mp3')
            window.display_status(status_label=self.__status_label, msg='Audio Download completed!')
        else:
            window.display_status(status_label=self.__status_label, msg='Error in Audio Download!')
