import json
import sqlite3
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
import Базовая_визуализация


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('change_film.ui', self)
        self.connection = sqlite3.connect("My_films.sqlite")

        with open("Константы.json", 'r') as file:
            data = json.load(file)
        self.change = data["change"]

        self.title.setText(self.change[1])
        self.director.setText(self.change[2])
        self.year.setText(self.change[3])
        spisok1 = [''] + [el[0] for el in self.connection.cursor().execute("SELECT genre FROM genres").fetchall()]
        self.genre.addItems(spisok1)
        self.genre.setCurrentIndex(spisok1.index(self.change[4]))
        self.duration.setText(self.change[5])
        spisok2 = ['', '1', '2', '3', '4', '5']
        self.rating.addItems(spisok2)
        self.rating.setCurrentIndex(spisok2.index(self.change[6]))

        self.other.clicked.connect(self.add_items)
        self.save.clicked.connect(self.save_result)

    def add_items(self):
        Базовая_визуализация.add_item(self)

    def save_result(self):
        if self.title.text():
            title = self.title.text()
        else:
            title = 'NULL'

        if self.director.text():
            try:
                director = int(self.connection.cursor().execute("SELECT id FROM authors where name = ?", (self.director.text(), )).fetchall()[0][0])
            except Exception:
                self.connection.cursor().execute(f"INSERT INTO directors(name) VALUES('{self.director.text()}')")
                self.connection.commit()
                director = int(self.connection.cursor().execute("SELECT id FROM authors where name = ?", (self.director.text(), )).fetchall()[0][0])
        else:
            director = 'NULL'

        if self.year.text():
            year = int(self.year.text())
        else:
            year = 'NULL'

        if self.genre.currentText():
            genre = int(self.connection.cursor().execute("SELECT id FROM genres where genre = ?", (self.genre.currentText(), )).fetchall()[0][0])
        else:
            genre = 'NULL'

        if self.duration.text():
            duration = int(self.duration.text())
        else:
            duration = 'NULL'

        if self.rating.currentText():
            rating = int(self.rating.currentText())
        else:
            rating = 'NULL'

        query = f"""UPDATE films SET
        title = '{title}', director = {director}, year = {year}, genre = {genre}, duration = {duration}, rating = {rating} WHERE id = ?"""
        print(query)
        self.connection.cursor().execute(query, (int(self.change[0]), ))
        self.connection.commit()

        with open("Константы.json", 'r') as file:
            data = json.load(file)

        QMessageBox.question(self, '', '\n'.join(["<b>Фильм с параметрами</b>:", f"название: {data[1]}", f"режиссёр: {data[2]}", f"год: {data[3]}",
                 f"жанр: {data[4]}", f"продолжительность: {data[5]}", f"рейтинг: {data[6]}", "<b>успешно заменён на фильм с параметрами:</b>"]) + '\n' + '\n'.join(
                [f"название: {title}", f"режиссёр: {director}", f"год: {year}",
                 f"жанр: {genre}", f"продолжительность: {duration}", f"рейтинг: {rating}"]))
        self.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())