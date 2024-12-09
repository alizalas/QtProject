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
        title = self.title.text()
        director = self.director.text()
        year = self.year.text()
        genre = self.genre.currentText()
        duration = self.duration.text()
        rating = self.rating.currentText()
        self.title.setText(self.change[1])
        self.director.setText(self.connection.cursor().execute("SELECT name FROM directors where id = ?", (self.change[2], )).fetchall()[0][0])
        self.year.setText(self.change[3])
        spisok1 = [''] + [el[0] for el in self.connection.cursor().execute("SELECT genre FROM genres").fetchall()]
        self.genre.addItems(spisok1)
        genre = self.connection.cursor().execute("SELECT genre FROM genres where id = ?", (self.change[4], )).fetchall()[0][0]
        self.genre.setCurrentIndex(spisok1.index(genre))
        self.duration.setText(self.change[5])
        spisok2 = ['', '1', '2', '3', '4', '5']
        self.rating.addItems(spisok2)
        genre = self.connection.cursor().execute("SELECT genre FROM genres where id = ?", (self.change[4],)).fetchall()[0][0]
        self.rating.setCurrentIndex(spisok2.index(genre))

        self.other.clicked.connect(self.add_items)
        self.save.clicked.connect(self.save_result)

    def add_items(self):
        Базовая_визуализация.add_item(self)

    def save_result(self):
        title = self.title.text()
        author = int(self.connection.cursor().execute("SELECT id FROM authors where name = ?", (self.author.text(), )).fetchall()[0][0])
        year = int(self.year.text())
        genre = int(self.connection.cursor().execute("SELECT id FROM genres where genre = ?", (self.genre.currentText(), )).fetchall()[0][0])

        spisok1 = [title, author, year, genre]
        spisok2 = ['title', 'author', 'year', 'genre']
        query = "UPDATE books SET\n"
        query += ", ".join([f"{key}={spisok1[spisok2.index(key)]}"
                          for key in spisok2])
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