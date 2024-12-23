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
        Базовая_визуализация.set_background_image(self)
        Базовая_визуализация.set_font_size(self)

        self.connection = sqlite3.connect("My_books.sqlite")

        with open("Константы.json", 'r') as file:
            data = json.load(file)
        self.change = data["change"]

        self.title.setText(self.change[1])
        self.author.setText(self.change[2])
        self.author.setCompleter(Базовая_визуализация.set_compliter(self, "authors"))
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

        QMessageBox.question(
            self, '', "<i>Книга с параметрами:</i>" + '<p>' + '<br>'.join(
                [f"<b>название:</b> {self.change[1]}", f"<b>автор:</b> {self.change[2]}", f"<b>год:</b> {self.change[3]}", f"<b>жанр:</b> {self.change[4]}"]) + '<p>' +
                 "успешно заменена на <i>книгу с параметрами:</i>" + '<p>' + '<br>'.join(
                [f"<b>название:</b> {self.title.text()}", f"<b>автор:</b> {self.author.text()}", f"<b>год:</b> {self.year.text()}", f"<b>жанр:</b> {self.genre.currentText()}"]))
        self.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
