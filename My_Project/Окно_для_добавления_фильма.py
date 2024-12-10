import sqlite3
import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow
import Базовая_визуализация


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('add_film.ui', self)
        self.connection = sqlite3.connect("My_films.sqlite")

        self.genre.addItems([''] + [el[0] for el in self.connection.cursor().execute("SELECT genre FROM genres").fetchall()])
        self.rating.addItems(['', '1', '2', '3', '4', '5'])

        self.other.clicked.connect(self.add_item)
        self.add.clicked.connect(self.add_film)

    def add_film(self):
        title = self.title.text()
        director = self.director.text()
        year = self.year.text()
        genre = self.genre.currentText()
        duration = self.duration.text()
        rating = self.rating.currentText()

        if title:
            query = f"INSERT INTO films(title, director, year, genre, duration, rating) VALUES('{title}', "
        else:
            query = f"INSERT INTO films(title, director, year, genre, duration, rating) VALUES({''}, "

        if director:
            try:
                result = int(
                    self.connection.cursor().execute("select id from directors where name = ?", (director, )).fetchall()[0][0])
            except Exception:
                self.connection.cursor().execute(f"INSERT INTO directors(name) VALUES('{director}')")
                self.connection.commit()
                result = int(
                    self.connection.cursor().execute(f"select id from directors where name = ?", (director, )).fetchall()[0][0])
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
            query += f"{result}, "
        else:
            query += f"{0}, "

        if duration:
            query += f"{int(duration)}, "
        else:
            query += f"{0}, "

        if rating:
            query += f"{int(rating)})"
        else:
            query += f"{0})"

        self.connection.cursor().execute(query)
        self.connection.commit()
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