import sqlite3
import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('add_book.ui', self)
        self.connection = sqlite3.connect("My_books.sqlite")
        self.add.clicked.connect(self.add_book)
        self.genre.addItems([el[0] for el in self.connection.cursor().execute("SELECT genre FROM genres").fetchall()])

    def add_book(self):
        id = self.id.text()
        title = self.title.text()
        author = self.author.text()
        year = self.year.text()
        genre = self.genre.text()

        if id:
            query = f"INSERT INTO books(id, title, author, year, genre) VALUES({id}, "
        else:
            query = "INSERT INTO books(title, author, year, genre) VALUES("

        if title:
            query += f"{title}, "
        else:
            query += "'', "

        if author:
            query += f"{author}, "
        else:
            query += "'', "

        if year:
            query += f"{int(year)}, "
        else:
            query += "'', "

        if genre:
            query += f"{genre})"
        else:
            query += "'')"

        self.connection.cursor().execute(query)
        self.connection.commit()

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