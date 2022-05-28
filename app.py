from PyQt6.QtWidgets import QApplication
from window import Window
import sys


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
