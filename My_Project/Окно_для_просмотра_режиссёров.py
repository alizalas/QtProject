import json
import sqlite3
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow
from My_Project import Базовая_визуализация, Менеджер_окон


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('select_directors.ui', self)

        Базовая_визуализация.set_background_image(self)
        Базовая_визуализация.set_font_size(self)

        self.connection = sqlite3.connect("My_films.sqlite")

        with open("Константы.json", 'r') as file:
            data = json.load(file)["font"]

        for i in range(1, 34):
            button = getattr(self, f'pushButton_{i}')
            button.setMinimumSize(data * 3, data * 3)
            button.clicked.connect(self.selection_by_letter)

        self.all_directors.clicked.connect(self.select_all)
        self.returne.clicked.connect(self.go_back)

    def select_all(self):
        query = f"""SELECT * FROM directors"""
        self.realisation(self.connection.cursor().execute(query).fetchall())

    def selection_by_letter(self):
        query = f"""SELECT * FROM directors 
                     WHERE name like '{self.sender().text()}%'"""
        self.realisation(self.connection.cursor().execute(query).fetchall())

    def realisation(self, res):
        headers = ['id', 'режиссёр']
        Базовая_визуализация.simple_realisation(self, res, headers, 2)

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
