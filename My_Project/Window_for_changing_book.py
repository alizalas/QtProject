import json
import sqlite3
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from My_Project import Basic_visualization, Window_manager


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('change_book.ui', self)

        Basic_visualization.set_background_image(self)
        Basic_visualization.set_font_size(self)

        self.connection = sqlite3.connect("My_books.sqlite")

        with open("Constants.json", 'r') as file:
            data = json.load(file)
        self.data = data["change"]

        self.title.setText(self.data[1])
        self.author.setText(self.data[2])
        self.author.setCompleter(Basic_visualization.set_compliter(self, "authors"))
        self.year.setText(self.data[3])
        spisok = [''] + [el[0] for el in self.connection.cursor().execute("SELECT genre FROM genres").fetchall()]
        self.genre.addItems(spisok)
        self.genre.setCurrentIndex(spisok.index(self.data[4]))
        self.link.setText(self.data[5])

        self.other.clicked.connect(self.add_item)
        self.save.clicked.connect(self.save_result)
        self.returne.clicked.connect(self.go_back)

    def save_result(self):
        if self.title.text():
            title = self.title.text()
        else:
            title = 'NULL'

        if self.author.text():
            try:
                author = int(
                    self.connection.cursor().execute("SELECT id FROM authors where name = ?",
                                                     (self.author.text(),)).fetchall()[0][0])
            except Exception:
                self.connection.cursor().execute(f"INSERT INTO authors(name) VALUES('{self.author.text()}')")
                self.connection.commit()
                author = int(
                    self.connection.cursor().execute("SELECT id FROM authors where name = ?",
                                                     (self.author.text(),)).fetchall()[0][0])
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

        if self.link.text():
            link = self.link.text()
        else:
            link = 'NULL'

        query = f"""UPDATE books SET
        title = '{title}', author = {author}, year = {year}, genre = {genre}, link = '{link}' WHERE id = ?"""
        self.connection.cursor().execute(query, (int(self.data[0]),))
        self.connection.commit()

        QMessageBox.question(
            self, '', "<i>Книга с параметрами:</i>" + '<p>' + '<br>'.join(
                [f"<b>название:</b> {self.data[1]}", f"<b>автор:</b> {self.data[2]}", f"<b>год:</b> {self.data[3]}",
                 f"<b>жанр:</b> {self.data[4]}", f"<b>ссылка:</b> {self.data[5]}"]) + '<p>' +
                      "успешно заменена на <i>книгу с параметрами:</i>" + '<p>' + '<br>'.join(
                [f"<b>название:</b> {self.title.text()}", f"<b>автор:</b> {self.author.text()}",
                 f"<b>год:</b> {self.year.text()}", f"<b>жанр:</b> {self.genre.currentText()}",
                 f"<b>ссылка:</b> {self.link.text()}"]))
        self.close()

    def add_item(self):
        Basic_visualization.add_item(self)

    def go_back(self):
        Window_manager.close_window(MyWidget)

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
