import json
import sqlite3
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow
from My_Project import Basic_visualization, Window_manager


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('select_genres.ui', self)

        Базовая_визуализация.set_background_image(self)
        Базовая_визуализация.set_font_size(self)

        with open("Constants.json", 'r') as file:
            data = json.load(file)

        if data["database"] == "books":
            self.connection = sqlite3.connect("My_books.sqlite")
        else:
            self.connection = sqlite3.connect("My_films.sqlite")

        for i in range(1, 34):
            button = getattr(self, f'pushButton_{i}')
            button.setMinimumSize(data["font"] * 3, data["font"] * 3)
            button.clicked.connect(self.selection_by_letter)

        self.all_genres.clicked.connect(self.select_all)
        self.returne.clicked.connect(self.go_back)

    def select_all(self):
        query = f"""SELECT * FROM genres"""
        self.realisation(self.connection.cursor().execute(query).fetchall())

    def selection_by_letter(self):
        query = f"""SELECT * FROM genres 
                     WHERE genre like '{self.sender().text()}%'"""
        self.realisation(self.connection.cursor().execute(query).fetchall())

    def realisation(self, res):
        headers = ['id', 'жанр']
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
