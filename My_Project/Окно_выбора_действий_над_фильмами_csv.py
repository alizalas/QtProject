import sqlite3
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from My_Project import Базовая_визуализация, Менеджер_окон


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('select_action_for_films-csv.ui', self)

        Базовая_визуализация.set_background_image(self)
        Базовая_визуализация.set_font_size(self)

        self.connection = sqlite3.connect("My_films.sqlite")

        self.choice.clicked.connect(self.choice_folder)
        self.returne.clicked.connect(self.go_back)

    def choice_folder(self):
        if self.films.isChecked():
            file_path = Базовая_визуализация.select_folder(self, "films-csv")
            data = self.connection.cursor().execute("SELECT * FROM films").fetchall()
            headers = ['id', 'название', 'режиссёр', 'год', 'жанр', 'продолжительность', 'рейтинг']
            Базовая_визуализация.make_csv(self, file_path, data, headers)

        elif self.directors.isChecked():
            file_path = Базовая_визуализация.select_folder(self, "directors-csv")
            data = self.connection.cursor().execute("SELECT * FROM directors").fetchall()
            headers = ['id', 'режиссёр']
            Базовая_визуализация.make_csv(self, file_path, data, headers)

        elif self.genres.isChecked():
            file_path = Базовая_визуализация.select_folder(self, "genres-csv")
            data = self.connection.cursor().execute("SELECT * FROM genres").fetchall()
            headers = ['id', 'жанр']
            Базовая_визуализация.make_csv(self, file_path, data, headers)

        else:
            QMessageBox.question(self, '', "Вы <b>не выбрали таблицу</b>, из которой хотите импортитовать данные")

    def go_back(self):
        Менеджер_окон.close_window(MyWidget)

    def closeEvent(self, event):
        self.connection.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
