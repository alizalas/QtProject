import json
import sqlite3
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow
import Window_manager
import Basic_visualization


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('../design/select_genres.ui', self)

        Basic_visualization.set_background_image(self)
        Basic_visualization.set_font_size(self)

        with open("../jsondir/Constants.json", 'r') as file:
            data = json.load(file)

        if data["database"] == "books":
            self.connection = sqlite3.connect("../databases/My_books.sqlite")
        else:
            self.connection = sqlite3.connect("../databases/My_films.sqlite")

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
        Basic_visualization.simple_realisation(self, res, headers, 2)

    def go_back(self):
        Window_manager.close_window(MyWidget)

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
