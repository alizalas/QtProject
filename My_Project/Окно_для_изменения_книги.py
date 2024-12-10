import json
import sqlite3
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow
import Базовая_визуализация


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('change_book.ui', self)
        self.connection = sqlite3.connect("My_books.sqlite")

        with open("Константы.json", 'r') as file:
            data = json.load(file)
        self.change = data["change"]
        self.title.setText(self.change[1])
        self.author.setText(self.change[2])
        self.year.setText(self.change[3])
        spisok = [''] + [el[0] for el in self.connection.cursor().execute("SELECT genre FROM genres").fetchall()]
        self.genre.addItems(spisok)
        self.genre.setCurrentIndex(spisok.index(self.change[4]))

        self.other.clicked.connect(self.add_items)
        self.save.clicked.connect(self.save_result)

    def add_items(self):
        Базовая_визуализация.add_item(self)

    def save_result(self):
        title = self.title.text()
        author = int(self.connection.cursor().execute("SELECT id FROM authors where name = ?", (self.author.text(), )).fetchall()[0][0])
        year = int(self.year.text())
        genre = int(self.connection.cursor().execute("SELECT id FROM genres where genre = ?", (self.genre.currentText(), )).fetchall()[0][0])

        query = f"""UPDATE books SET
        title = '{title}', author = {author}, year = {year}, genre = {genre} WHERE id = ?"""
        print(query)
        self.connection.cursor().execute(query, (int(self.change[0]), ))
        self.connection.commit()
        self.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())