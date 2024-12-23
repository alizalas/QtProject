import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow

import subprocess

from My_Project import Базовая_визуализация


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('select_action_for_films.ui', self)

        Базовая_визуализация.set_background_image(self)
        Базовая_визуализация.set_font_size(self)

        self.search.clicked.connect(self.click_handling)
        self.add.clicked.connect(self.click_handling)

    def click_handling(self):
        button_name = self.sender().objectName()
        if button_name == "search":
            subprocess.run([sys.executable, 'Окно_для_поиска_фильмов.py'])
        else:
            subprocess.run([sys.executable, 'Окно_для_добавления_фильма.py'])


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())