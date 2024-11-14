import sqlite3
import sys
import io

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('', self)
        self.connection = sqlite3.connect("My_films.sqlite")
        self.search.clicked.connect(self.select_data)

    def select_data(self):
        id = self.id.text()
        title = self.title.text()
        director = self.director.text()
        year = self.year.text()
        genre = self.genre.text()
        duration = self.duration.text()
        rating = self.rating.text()
        query = "SELECT * FROM films WHERE 1=1"

        if year:
            query += f" AND year {year}"

        if title:
            query += f" AND title {title}"

        if duration:
            query += f" AND duration {duration}"

        res = self.connection.cursor().execute(query).fetchall()

        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(['id', 'title', 'year', 'genre', 'duration'])

        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

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