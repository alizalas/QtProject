import json
import sqlite3
import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow
import subprocess
import Базовая_визуализация


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('add_film.ui', self)
        self.connection = sqlite3.connect("My_films.sqlite")
        self.add.clicked.connect(self.add_film)
        self.genre.addItems([''] + [el[0] for el in self.connection.cursor().execute("SELECT genre FROM genres").fetchall()])
        self.other.clicked.connect(self.add_item)
        self.rating.addItems(['', '1', '2', '3', '4', '5'])

    def add_film(self):
        title = self.title.text()
        director = self.director.text()
        year = self.year.text()
        genre = self.genre.currentText()
        duration = self.duration.text()
        rating = self.rating.currentText()

        if title:
            query = f"INSERT INTO films(title, director, year, genre, duration, rating) VALUES({title}, "
        else:
            query = f"INSERT INTO books(title, director, year, genre, duration, rating) VALUES({'NULL'}, "

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
                query += f"'{result}', "
        else:
            query += f"{'NULL'}, "

        if year:
            query += f"{int(year)}, "
        else:
            query += f"{'NULL'}, "

        if genre:
            try:
                result = int(
                    self.connection.cursor().execute(f"select id from genres where genre = ?", (genre, )).fetchall()[0][0])
            except:

                result = int(
                    self.connection.cursor().execute(f"select id from authors where name = ?", (genre, )).fetchall()[0][0])
            finally:
                query += f"{result}, "
        else:
            query += f"{'NULL'}, "

        if duration:
            query += f"{int(duration)}, "
        else:
            query += f"{'NULL'}, "

        if rating:
            query += f"{int(rating)})"
        else:
            query += f"{'NULL'})"

        self.connection.cursor().execute(query)
        self.connection.commit()

    def add_item(self):
        subprocess.run([sys.executable, 'Окно_добавления_значения.py'])
        with open("Константы.json", 'r') as file:
            data = json.load(file)
        self.genre.addItems([str(data["signalText"])])
        self.connection.cursor().execute(f"INSERT INTO genres(genre) VALUES({str(data['signalText'])})")
        self.connection.commit()

    def closeEvent(self, event):
        self.connection.close()


def signal(text):
    Базовая_визуализация.modify_variable_in_file("Константы.json", {"signalText": text})

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())