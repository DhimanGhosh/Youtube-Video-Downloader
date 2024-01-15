from PyQt6.QtWidgets import (
    QWidget
)
from PyQt6.QtGui import (
    QCursor
)
from PyQt6.QtCore import (
    Qt
)


def change_pointer_to_hand(widget: QWidget) -> None:
    widget.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))


def set_widget_color(widget: QWidget, color: str):
    widget.setStyleSheet(f'color: {color}')
