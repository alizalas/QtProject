import sqlite3
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from My_Project import Basic_visualization, Window_manager


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('add_book.ui', self)

        Basic_visualization.set_background_image(self)
        Basic_visualization.set_font_size(self)

        self.connection = sqlite3.connect("My_books.sqlite")

        self.author.setCompleter(Basic_visualization.set_compliter(self, "authors"))
        self.genre.addItems(
            [''] + [el[0] for el in self.connection.cursor().execute("SELECT genre FROM genres").fetchall()] + [
                "Другое..."])

        self.other.clicked.connect(self.add_item)
        self.add.clicked.connect(self.add_book)
        self.returne.clicked.connect(self.go_back)

    def add_book(self):
        title = self.title.text()
        author = self.author.text()
        year = self.year.text()
        genre = self.genre.currentText()
        link = self.link.text()

        if title:
            query = f"INSERT INTO books(title, author, year, genre, link) VALUES('{title}', "
        else:
            query = f"INSERT INTO books(title, author, year, genre, link) VALUES({'NULL'}, "

        if author:
            try:
                result = \
                    self.connection.cursor().execute("select id from authors where name = ?", (author,)).fetchall()[0][
                        0]
            except Exception:
                self.connection.cursor().execute(f"INSERT INTO authors(name) VALUES('{author}')")
                self.connection.commit()
                result = \
                    self.connection.cursor().execute(f"select id from authors where name = ?", (author,)).fetchall()[0][
                        0]
            finally:
                query += f"{int(result)}, "
        else:
            query += f"{'NULL'}, "

        if year:
            query += f"{int(year)}, "
        else:
            query += f"{'NULL'}, "

        if genre:
            result = self.connection.cursor().execute(f"select id from genres where genre = ?", (genre,)).fetchall()[0][
                0]
            query += f"{int(result)}, "
        else:
            query += f"{'NULL'}, "

        if link:
            query += f"'{link}')"
        else:
            query += f"{'NULL'})"

        self.connection.cursor().execute(query)
        self.connection.commit()
        QMessageBox.question(
            self, '', "<i>Книга с параметрами:</i>" + '<p>' + '<br>'.join(
                [f"<b>название:</b> {title}", f"<b>автор:</b> {author}", f"<b>год:</b> {year}", f"<b>жанр:</b> {genre}",
                 f"<b>ссылка:</b> {link}"]) + '<p>' + "добавлена в каталог")
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
