import json
import sqlite3
import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
import subprocess
import Базовая_визуализация


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('add_book.ui', self)
        self.connection = sqlite3.connect("My_books.sqlite")

        self.genre.addItems([''] + [el[0] for el in self.connection.cursor().execute("SELECT genre FROM genres").fetchall()] + ["Другое..."])
        self.other.clicked.connect(self.add_item)
        self.add.clicked.connect(self.add_book)

    def add_book(self):
        title = self.title.text()
        author = self.author.text()
        year = self.year.text()
        genre = self.genre.currentText()

        if title:
            query = f"INSERT INTO books(title, author, year, genre) VALUES('{title}', "
        else:
            query = f"INSERT INTO books(title, author, year, genre) VALUES({''}, "

        if author:
            try:
                result = int(
                    self.connection.cursor().execute("select id from authors where name = ?", (author, )).fetchall()[0][0])
            except Exception:
                self.connection.cursor().execute(f"INSERT INTO authors(name) VALUES('{author}')")
                self.connection.commit()
                result = int(
                    self.connection.cursor().execute(f"select id from authors where name = ?", (author, )).fetchall()[0][0])
            finally:
                query += f"{result}, "
        else:
            query += f"{0}, "

        if year:
            query += f"{int(year)}, "
        else:
            query += f"{0}, "

        if genre:
            result = int(
                    self.connection.cursor().execute(f"select id from genres where genre = ?", (genre, )).fetchall()[0][0])
            query += f"{result})"
        else:
            query += f"{0})"

        self.connection.cursor().execute(query)
        self.connection.commit()
        QMessageBox.question(
            self, '', '\n'.join(["Книга с параметрами: ", f"название: {title}", f"автор: {author}", f"год: {year}", f"жанр: {genre}", "добавлена в каталог"]))
        self.close()

    def add_item(self):
        Базовая_визуализация.add_item(self)

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