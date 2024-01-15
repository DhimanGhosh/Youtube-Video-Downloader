from PyQt6.QtWidgets import QApplication
from qt_material import apply_stylesheet
from window import Window
import sys


if __name__ == '__main__':
    """
    Possible Themes:
        'dark_amber.xml', 'dark_blue.xml', 'dark_cyan.xml', 'dark_lightgreen.xml',
        'dark_pink.xml', 'dark_purple.xml', 'dark_red.xml', 'dark_teal.xml',
        'dark_yellow.xml', 'light_amber.xml', 'light_blue.xml', 'light_blue_500.xml',
        'light_cyan.xml', 'light_cyan_500.xml', 'light_lightgreen.xml', 'light_lightgreen_500.xml',
        'light_orange.xml', 'light_pink.xml', 'light_pink_500.xml', 'light_purple.xml',
        'light_purple_500.xml', 'light_red.xml', 'light_red_500.xml', 'light_teal.xml',
        'light_teal_500.xml', 'light_yellow.xml'
    """
    # create the application and the main window
    app = QApplication(sys.argv)
    my_app = Window()

    # setup stylesheet
    apply_stylesheet(app, theme='light_teal_500.xml')

    # run
    my_app.show()
    sys.exit(app.exec())
