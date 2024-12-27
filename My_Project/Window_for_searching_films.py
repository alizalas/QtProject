import json
import sqlite3
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow
import Basic_visualization, Window_manager


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('select_films.ui', self)

        Basic_visualization.set_background_image(self)
        Basic_visualization.set_font_size(self)

        self.connection = sqlite3.connect("My_films.sqlite")

        self.director.setCompleter(Basic_visualization.set_compliter(self, "directors"))
        self.genre.addItems(
            [''] + [el[0] for el in self.connection.cursor().execute("SELECT genre FROM genres").fetchall()])
        self.rating.addItems(['', '1', '2', '3', '4', '5'])

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
        director = self.director.text()
        year = self.year.text()
        genre = self.genre.currentText()
        duration = self.duration.text()
        rating = self.rating.currentText()
        link = self.link.text()
        query = """SELECT films.id, films.title, directors.name, films.year, genres.genre, films.duration, films.rating, films.link 
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

        if link:
            query += f" AND films.link = '{link}'"

        self.realisation(self.connection.cursor().execute(query).fetchall())

    def selection_by_letter(self):
        query = f"""SELECT films.id, films.title, directors.name, films.year, genres.genre, films.duration, films.rating, films.link 
                     FROM films 
                     LEFT JOIN directors ON directors.id = films.director
                     LEFT JOIN genres ON genres.id = films.genre
                     WHERE films.title like '{self.sender().text()}%'"""
        self.realisation(self.connection.cursor().execute(query).fetchall())

    def realisation(self, res):
        headers = ['id', 'название', 'режиссёр', 'год', 'жанр', 'продолжительность', 'рейтинг', 'ссылка']
        Basic_visualization.realisation_with_additional_features(self, res, headers, 8)

    def open_link(self, row, col):
        Basic_visualization.open_link(self, row, col)

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
