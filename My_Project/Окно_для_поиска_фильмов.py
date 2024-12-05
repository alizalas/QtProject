import sqlite3
import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
import json


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('select_films.ui', self)
        self.connection = sqlite3.connect("My_films.sqlite")
        self.search.clicked.connect(self.selection_by_characteristics)
        for i in range(1, 34):
            button = getattr(self, f'pushButton_{i}')
            button.clicked.connect(self.selection_by_letter)
        self.genre.addItems([el[0] for el in self.connection.cursor().execute("SELECT genre FROM genres").fetchall()])
        self.rating.addItems(['1', '2', '3', '4', '5'])

    def selection_by_characteristics(self):
        id = self.id.text()
        title = self.title.text()
        director = self.director.text()
        year = self.year.text()
        genre = self.genre.text()
        duration = self.duration.text()
        rating = self.rating.text()
        query = "SELECT * FROM films WHERE 1=1"

        if id:
            query += f" AND id = {int(id)}"

        if title:
            query += f" AND title = {title}"

        if director:
            query += f" AND director = (select id from directors where name = {director})"

        if year:
            query += f" AND year = {int(year)}"

        if genre:
            query += f" AND genre = (select id from genres where genre = {genre})"

        if duration:
            query += f" AND duration = {int(duration)}"

        if rating:
            query += f" AND rating = {int(rating)}"

        self.realisation(self.connection.cursor().execute(query).fetchall())

    def selection_by_letter(self):
        query = f"SELECT * FROM films WHERE title like '{self.sender().text()}%'"
        self.realisation(self.connection.cursor().execute(query).fetchall())

    def realisation(self, res):
        if res:
            self.tableWidget.setColumnCount(7)
            self.tableWidget.setRowCount(0)
            self.tableWidget.setHorizontalHeaderLabels(['id', 'title', 'director', 'year', 'genre', 'duration', 'rating'])

            for i, row in enumerate(res):
                self.tableWidget.setRowCount(
                    self.tableWidget.rowCount() + 1)
                for j, elem in enumerate(row):
                    self.tableWidget.setItem(
                        i, j, QTableWidgetItem(str(elem)))
            self.table.resizeColumnsToContents()
        else:
            self.statusBar().showMessage('Ничего не нашлось')

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