import sqlite3
import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow
import Базовая_визуализация


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('select_books.ui', self)
        self.connection = sqlite3.connect("My_books.sqlite")

        self.genre.addItems(
            [''] + [el[0] for el in self.connection.cursor().execute("SELECT genre FROM genres").fetchall()])

        for i in range(1, 34):
            button = getattr(self, f'pushButton_{i}')
            button.clicked.connect(self.selection_by_letter)
        self.search.clicked.connect(self.selection_by_characteristics)

    def selection_by_characteristics(self):
        title = self.title.text()
        author = self.author.text()
        year = self.year.text()
        genre = self.genre.currentText()
        query = "SELECT * FROM books WHERE 1=1"

        if title:
            query += f" AND title = '{title}'"

        if author:
            query += f" AND author = (select id from author where name = '{author}')"

        if year:
            query += f" AND year = {int(year)}"

        if genre:
            query += f" AND genre = (select id from genres where genre = '{genre}')"

        self.realisation(self.connection.cursor().execute(query).fetchall())

    def selection_by_letter(self):
        query = f"SELECT * FROM books WHERE title like '{self.sender().text()}%'"
        self.realisation(self.connection.cursor().execute(query).fetchall())

    def realisation(self, res):
        headers = ['id', 'title', 'author', 'year', 'genre']
        Базовая_визуализация.realisation(self, res, headers, 5)

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