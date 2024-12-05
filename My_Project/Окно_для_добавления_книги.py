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
        uic.loadUi('add_book.ui', self)
        self.connection = sqlite3.connect("My_books.sqlite")
        self.add.clicked.connect(self.add_book)
        self.genre.addItems([''] + [el[0] for el in self.connection.cursor().execute("SELECT genre FROM genres").fetchall()] + ["Другое..."])
        self.other.clicked.connect(self.add_item)

    def add_book(self):
        title = self.title.text()
        author = self.author.text()
        year = self.year.text()
        genre = self.genre.currentText()

        if title:
            query = f"INSERT INTO books(title, author, year, genre) VALUES('{title}', "
        else:
            query = f"INSERT INTO books(title, author, year, genre) VALUES({'NULL'}, "

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
                query += f"'{result}', "
        else:
            query += f"{'NULL'}, "

        if year:
            query += f"{int(year)}, "
        else:
            query += f"{'NULL'}, "

        if genre:
            result = int(
                    self.connection.cursor().execute(f"select id from genres where genre = ?", (genre, )).fetchall()[0][0])
            query += f"{result})"
        else:
            query += f"{'NULL'})"

        self.connection.cursor().execute(query)
        self.connection.commit()
        self.close()

    def add_item(self):
        subprocess.run([sys.executable, 'Окно_добавления_значения.py'])
        with open("Константы.json", 'r') as file:
            data = json.load(file)
        self.genre.addItems([str(data["signalText"])])
        self.connection.cursor().execute(f"INSERT INTO genres(genre) VALUES('{data['signalText']}')")
        self.connection.commit()

    def closeEvent(self, event):
        self.connection.close()


def signal(text):
    print(text)
    Базовая_визуализация.modify_variable_in_file("Константы.json", {"signalText": text})

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())