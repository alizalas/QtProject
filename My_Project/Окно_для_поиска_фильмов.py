import sqlite3
import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
import Базовая_визуализация


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('select_films.ui', self)

        Базовая_визуализация.set_background_image(self)
        Базовая_визуализация.set_font_size(self)

        self.connection = sqlite3.connect("My_films.sqlite")

        self.director.setCompleter(Базовая_визуализация.set_compliter(self, "directors"))
        self.genre.addItems(
            [''] + [el[0] for el in self.connection.cursor().execute("SELECT genre FROM genres").fetchall()])
        self.rating.addItems(['', '1', '2', '3', '4', '5'])

        for i in range(1, 34):
            button = getattr(self, f'pushButton_{i}')
            button.clicked.connect(self.selection_by_letter)
        self.search.clicked.connect(self.selection_by_characteristics)
        self.returne.clicked.connect(self.close)

    def selection_by_characteristics(self):
        title = self.title.text()
        director = self.director.text()
        year = self.year.text()
        genre = self.genre.currentText()
        duration = self.duration.text()
        rating = self.rating.currentText()
        query = """SELECT films.id, films.title, directors.name, films.year, genres.genre, films.duration, films.rating 
                     FROM films 
                     LEFT JOIN directors ON directors.id = films.director
                     LEFT JOIN genres ON genres.id = films.genre
                     WHERE 1=1"""

        if title:
            query += f" AND films.title = '{title}'"

        if director:
            query += f" AND directors.name = '{director}'"

        if year:
            query += f" AND films.year = {int(year)}"

        if genre:
            query += f" AND genres.genre = '{genre}'"

        if duration:
            query += f" AND films.duration = {int(duration)}"

        if rating:
            query += f" AND films.rating = {int(rating)}"

        self.realisation(self.connection.cursor().execute(query).fetchall())

    def selection_by_letter(self):
        query = f"""SELECT films.id, films.title, directors.name, films.year, genres.genre, films.duration, films.rating 
                     FROM films 
                     LEFT JOIN directors ON directors.id = films.director
                     LEFT JOIN genres ON genres.id = films.genre
                     WHERE films.title like '{self.sender().text()}%'"""
        self.realisation(self.connection.cursor().execute(query).fetchall())

    def realisation(self, res):
        headers = ['id', 'название', 'режиссёр', 'год', 'жанр', 'продолжительность', 'рейтинг']
        Базовая_визуализация.realisation(self, res, headers, 7)

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