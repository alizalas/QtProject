import subprocess
import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow
import Базовая_визуализация


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('first_window.ui', self)
        self.setWindowTitle("Начальное окно")
        self.books.setToolTip("Здесь можно работать с каталогом <b>книг</b>")
        self.films.setToolTip("Здесь можно работать с каталогом <b>фильмов</b>")
        self.reference.setToolTip("Здесь можно больше узнать о нашем <b>приложении</b>")
        self.settings.setToolTip("Здесь можно изменить настройки окон")
        self.exit.setToolTip("Выйти из приложения")

        Базовая_визуализация.set_background_image(self)
        Базовая_визуализация.set_font(self)
        self.books.clicked.connect(self.open_next_window)
        self.films.clicked.connect(self.open_next_window)
        self.reference.clicked.connect(self.open_next_window)
        self.settings.clicked.connect(self.open_next_window)
        self.exit.clicked.connect(self.open_next_window)


    def open_next_window(self):
        button_name = self.sender().objectName()
        if button_name == "books":
            subprocess.run([sys.executable, 'Окно_выбора_действий_над_книгами.py'])
        elif button_name == "films":
            subprocess.run([sys.executable, 'Окно_выбора_действий_над_фильмами.py'])
        elif button_name == "reference":
            subprocess.run([sys.executable, 'Окно_справки.py'])
        elif button_name == "settings":
            subprocess.run([sys.executable, 'Окно_настроек.py'])
        else:
            self.close()

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())