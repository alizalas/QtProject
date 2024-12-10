import json
import sqlite3
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow
import Базовая_визуализация


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('change_film.ui', self)
        self.connection = sqlite3.connect("My_films.sqlite")

        with open("Константы.json", 'r') as file:
            data = json.load(file)
        self.change = data["change"]

        self.title.setText(self.change[1])
        self.director.setText(self.change[2])
        self.year.setText(self.change[3])
        spisok1 = [''] + [el[0] for el in self.connection.cursor().execute("SELECT genre FROM genres").fetchall()]
        self.genre.addItems(spisok1)
        self.genre.setCurrentIndex(spisok1.index(self.change[4]))
        self.duration.setText(self.change[5])
        spisok2 = ['', '1', '2', '3', '4', '5']
        self.rating.addItems(spisok2)
        self.rating.setCurrentIndex(spisok2.index(self.change[6]))

        self.other.clicked.connect(self.add_items)
        self.save.clicked.connect(self.save_result)

    def add_items(self):
        Базовая_визуализация.add_item(self)

    def save_result(self):
        title = self.title.text()
        director = int(self.connection.cursor().execute("SELECT id FROM authors where name = ?", (self.director.text(), )).fetchall()[0][0])
        year = int(self.year.text())
        genre = int(self.connection.cursor().execute("SELECT id FROM genres where genre = ?", (self.genre.currentText(), )).fetchall()[0][0])
        duration = int(self.duration.text())
        rating = int(self.rating.currentText())

        spisok1 = [title, director, year, genre, duration, rating]
        spisok2 = ['title', 'director', 'year', 'genre', 'duration', 'rating']
        query = f"""UPDATE films SET
        title = '{title}', author = {author}, year = {year}, genre = {genre} WHERE id = ?"""
        query += "WHERE id = ?"
        print(query)
        self.connection.cursor().execute(query, (int(self.change[0]), ))
        self.connection.commit()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())