import csv
import sqlite3
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from My_Project import Базовая_визуализация


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('select_action_for_books-scv.ui', self)
        self.connection = sqlite3.connect("My_books.sqlite")

        Базовая_визуализация.set_background_image(self)
        Базовая_визуализация.set_font_size(self)

        self.choice.clicked.connect(self.choice_folder)
        self.returne.clicked.connect(self.close)

    def choice_folder(self):
        if self.books.isChecked():
            file_path = Базовая_визуализация.select_folder(self, "books-csv")
            data = self.connection.cursor().execute("SELECT * FROM books").fetchall()
            headers = ['id', 'название', 'автор', 'год', 'жанр', 'ссылка']
            self.make_csv(file_path, data, headers)

        elif self.authors.isChecked():
            file_path = Базовая_визуализация.select_folder(self, "authors-csv")
            data = self.connection.cursor().execute("SELECT * FROM authors").fetchall()
            headers = ['id', 'автор']
            self.make_csv(file_path, data, headers)

        elif self.genres.isChecked():
            file_path = Базовая_визуализация.select_folder(self, "genres-csv")
            data = self.connection.cursor().execute("SELECT * FROM genres").fetchall()
            headers = ['id', 'жанр']
            self.make_csv(file_path, data, headers)

        else:
            QMessageBox.question(self, '', "Вы не выбрали таблицу, из которой хотите импортитовать данные")

        self.close()

    def make_csv(self, file_path, data, headers):
        if data:
            with open(file_path, 'w', newline='', encoding="utf8") as csvfile:
                writer = csv.writer(
                    csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(headers)
                for row in data:
                    writer.writerow(list(row))

            QMessageBox.question(self, '', f"Данные из выбранной Вами таблицы <b>успешно сохранены</b> по <i>пути</i>:<p>{file_path}")

        else:
            QMessageBox.question(self, '', "В выбранной Вами таблице <b>нет данных</b>")


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())