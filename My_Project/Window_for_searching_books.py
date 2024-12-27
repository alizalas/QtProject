import json
import sqlite3
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow
from My_Project import Basic_visualization, Window_manager


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('select_books.ui', self)

        Базовая_визуализация.set_background_image(self)
        Базовая_визуализация.set_font_size(self)

        self.connection = sqlite3.connect("My_books.sqlite")

        self.author.setCompleter(Базовая_визуализация.set_compliter(self, "authors"))
        self.genre.addItems(
            [''] + [el[0] for el in self.connection.cursor().execute("SELECT genre FROM genres").fetchall()])

        with open("Constants.json", 'r') as file:
            data = json.load(file)["font"]

        for i in range(1, 34):
            button = getattr(self, f'pushButton_{i}')
            button.setMinimumSize(data * 3, data * 3)
            button.clicked.connect(self.selection_by_letter)

        self.search.clicked.connect(self.selection_by_characteristics)
        self.returne.clicked.connect(self.go_back)

    def selection_by_characteristics(self):
        title = self.title.text()
        author = self.author.text()
        year = self.year.text()
        genre = self.genre.currentText()
        link = self.link.text()
        query = """SELECT books.id, books.title, authors.name, books.year, genres.genre, books.link 
                   FROM books 
                   LEFT JOIN authors ON authors.id = books.author
                   LEFT JOIN genres ON genres.id = books.genre
                   WHERE 1=1"""

        if title:
            query += f" AND books.title = '{title}'"

        if author:
            query += f" AND authors.name = '{author}'"

        if year:
            query += f" AND books.year = {int(year)}"

        if genre:
            query += f" AND genres.genre = '{genre}'"

        if link:
            query += f" AND books.link = '{link}'"

        self.realisation(self.connection.cursor().execute(query).fetchall())

    def selection_by_letter(self):
        query = f"""SELECT books.id, books.title, authors.name, books.year, genres.genre, books.link 
                     FROM books 
                     LEFT JOIN authors ON authors.id = books.author
                     LEFT JOIN genres ON genres.id = books.genre
                     WHERE books.title like '{self.sender().text()}%'"""
        self.realisation(self.connection.cursor().execute(query).fetchall())

    def realisation(self, res):
        headers = ['id', 'название', 'автор', 'год', 'жанр', 'ссылка']
        Базовая_визуализация.realisation_with_additional_features(self, res, headers, 6)

    def open_link(self, row, col):
        Базовая_визуализация.open_link(self, row, col)

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
