from PyQt6.QtWidgets import (
    QLabel
)
from time import sleep

DISPLAY_STATUS_WAIT_TIME = 5


def display_status(status_label: QLabel, msg: str, wait_time: int = 0) -> None:
    status_label.setText(msg)
    if not wait_time:
        wait_time = DISPLAY_STATUS_WAIT_TIME
    sleep(wait_time)
    status_label.clear()
