import json
import sqlite3
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
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
        if self.title.text():
            title = self.title.text()
        else:
            title = 'NULL'

        if self.author.text():
            try:
                author = int(
                    self.connection.cursor().execute("SELECT id FROM authors where name = ?", (self.author.text(),)).fetchall()[
                        0][0])
            except Exception:
                self.connection.cursor().execute(f"INSERT INTO authors(name) VALUES('{self.author.text()}')")
                self.connection.commit()
                author = int(
                    self.connection.cursor().execute("SELECT id FROM authors where name = ?",
                                                     (self.author.text(),)).fetchall()[
                        0][0])
        else:
            author = 'NULL'

        if self.year.text():
            year = int(self.year.text())
        else:
            year = 'NULL'

        if self.genre.currentText():
            genre = int(self.connection.cursor().execute("SELECT id FROM genres where genre = ?",
                                                     (self.genre.currentText(),)).fetchall()[0][0])
        else:
            genre = 'NULL'

        query = f"""UPDATE books SET
        title = '{title}', author = {author}, year = {year}, genre = {genre} WHERE id = ?"""
        print(query)
        self.connection.cursor().execute(query, (int(self.change[0]),))
        self.connection.commit()

        with open("Константы.json", 'r') as file:
            data = json.load(file)["change"]

        QMessageBox.question(
            self, '', '<p>'.join(
                ["<b>Книга с параметрами: </b>", f"название: {data[1]}", f"автор: {data[2]}", f"год: {data[3]}", f"жанр: {data[4]}",
                 "успешно заменена на книгу с параметрами:"]) + '\n' + '<br>'.join(
                [f"название: {title}", f"автор: {author}", f"год: {year}", f"жанр: {genre}"]))
        self.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
