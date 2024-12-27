import sqlite3
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from My_Project import Basic_visualization, Window_manager


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('add_film.ui', self)

        Basic_visualization.set_background_image(self)
        Basic_visualization.set_font_size(self)

        self.connection = sqlite3.connect("My_films.sqlite")

        self.director.setCompleter(Basic_visualization.set_compliter(self, "directors"))
        self.genre.addItems(
            [''] + [el[0] for el in self.connection.cursor().execute("SELECT genre FROM genres").fetchall()])
        self.rating.addItems(['', '1', '2', '3', '4', '5'])

        self.other.clicked.connect(self.add_item)
        self.add.clicked.connect(self.add_film)
        self.returne.clicked.connect(self.go_back)

    def add_film(self):
        title = self.title.text()
        director = self.director.text()
        year = self.year.text()
        genre = self.genre.currentText()
        duration = self.duration.text()
        rating = self.rating.currentText()
        link = self.link.text()

        if title:
            query = f"INSERT INTO films(title, director, year, genre, duration, rating, link) VALUES('{title}', "
        else:
            query = f"INSERT INTO films(title, director, year, genre, duration, rating, link) VALUES({'NULL'}, "

        if director:
            try:
                result = \
                    self.connection.cursor().execute("select id from directors where name = ?", (director,)).fetchall()[
                        0][0]
            except Exception:
                self.connection.cursor().execute(f"INSERT INTO directors(name) VALUES('{director}')")
                self.connection.commit()
                result = self.connection.cursor().execute(f"select id from directors where name = ?",
                                                          (director,)).fetchall()[0][0]
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

        if duration:
            query += f"{int(duration)}, "
        else:
            query += f"{'NULL'}, "

        if rating:
            query += f"{int(rating)}, "
        else:
            query += f"{'NULL'}, "

        if link:
            query += f"'{link}')"
        else:
            query += f"{'NULL'})"

        self.connection.cursor().execute(query)
        self.connection.commit()
        QMessageBox.question(
            self, '', "<i>Фильм с параметрами:</i>" + '<p>' + '<br>'.join(
                [f"<b>название:</b> {title}", f"<b>режиссёр:</b> {director}", f"<b>год:</b> {year}",
                 f"<b>жанр:</b> {genre}", f"<b>продолжительность:</b> {duration}", f"<b>рейтинг:</b> {rating}",
                 f"<b>ссылка:</b> {link}"]) + '<p>' + "добавлен в каталог")
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
