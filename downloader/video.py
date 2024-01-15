from PyQt6.QtWidgets import (
    QLineEdit
)
import urllib.request
import re
import os
import shutil


def get_video_title(url: str) -> str:
    response = urllib.request.urlopen(url)
    html_content = response.read().decode('utf-8', errors='ignore')

    # Extract the video title from the HTML content
    match = re.search('<title>(.*?) - YouTube</title>', html_content)
    title = 'Title not found'
    if match:
        title = match.group(1)
    return title


def move_to(save_to_path: QLineEdit, downloaded_file: str, media_extension='.mp4') -> None:
    move_to_path = save_to_path.text()
    if move_to_path:
        if '.' not in move_to_path.split(os.sep)[-1]:  # if file extension not specified
            move_to_path += media_extension
        if move_to_path.split(os.sep)[-1].split('.')[-1] != media_extension[1:]:  # if incorrect file extension specified
            move_to_path = os.sep.join(move_to_path.split(os.sep)[:-1]) + os.sep + \
                           move_to_path.split(os.sep)[-1].split('.')[0] + media_extension
        shutil.copy(downloaded_file, move_to_path)
        os.remove(downloaded_file)
