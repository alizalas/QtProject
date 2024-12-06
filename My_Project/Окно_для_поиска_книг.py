import sqlite3
import subprocess
import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QLineEdit, QPushButton
import Базовая_визуализация


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('select_books.ui', self)
        self.connection = sqlite3.connect("My_books.sqlite")
        self.search.clicked.connect(self.selection_by_characteristics)
        for i in range(1, 34):
            button = getattr(self, f'pushButton_{i}')
            button.clicked.connect(self.selection_by_letter)
        self.genre.addItems([''] + [el[0] for el in self.connection.cursor().execute("SELECT genre FROM genres").fetchall()])

    def selection_by_characteristics(self):
        id = self.id.text()
        title = self.title.text()
        author = self.author.text()
        year = self.year.text()
        genre = self.genre.currentText()
        query = "SELECT * FROM books WHERE 1=1"

        if id:
            query += f" AND id = {int(id)}"

        if title:
            query += f" AND title = {title}"

        if author:
            query += f" AND author = (select id from author where name = {author})"

        if year:
            query += f" AND year = {int(year)}"

        if genre:
            query += f" AND genre = (select id from genres where genre = {genre})"

        self.realisation(self.connection.cursor().execute(query).fetchall())

    def selection_by_letter(self):
        query = f"SELECT * FROM books WHERE title like '{self.sender().text()}%'"
        self.realisation(self.connection.cursor().execute(query).fetchall())

    def realisation(self, res):
        if res:
            self.tableWidget.setColumnCount(7)
            self.tableWidget.setRowCount(0)
            self.tableWidget.setHorizontalHeaderLabels(['id', 'title', 'author', 'year', 'genre', 'редактировать', 'удалить'])

            for i, row in enumerate(res):
                self.tableWidget.setRowCount(
                    self.tableWidget.rowCount() + 1)

                num = self.tableWidget.rowCount() - 1

                edit = QPushButton("Редактировать", self)
                edit.clicked.connect(
                    lambda checked, num=num: self.edit_film(num))  # Передача номера строки через лямбда-функцию
                self.tableWidget.setCellWidget(num, 5, edit)

                delete = QPushButton("Удалить")
                delete.clicked.connect(
                    lambda checked, num=num: self.delete_film(num))  # Передача номера строки через лямбда-функцию
                self.tableWidget.setCellWidget(num, 6, delete)

                for j, elem in enumerate(row):
                    self.tableWidget.setItem(
                        i, j, QTableWidgetItem(str(elem)))

            self.tableWidget.resizeColumnsToContents()
        else:
            self.statusBar().showMessage('Ничего не нашлось')

    def edit_film(self, num):
        print(f"Редактирование фильма в строке {num}")
        row_values = [self.tableWidget.item(num, col).text() for col in range(5)]
        Базовая_визуализация.modify_variable_in_file("Константы.json", {"changeBook": row_values})
        #subprocess.run([sys.executable, 'Окно_для_изменения_книги2.py'])
        # Здесь реализуйте логику редактирования фильма
        # Например, откройте диалоговое окно для редактирования данных

    def delete_film(self, num):
        print(f"Удаление фильма в строке {num}")
        row_values = [self.tableWidget.item(num, col).text() for col in range(5)]
        self.tableWidget.removeRow(num)
        # Здесь реализуйте логику удаления фильма

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