import csv
import sqlite3
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog

import subprocess

from My_Project import Базовая_визуализация


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('select_action_for_books-scv.ui', self)
        self.connection = sqlite3.connect("My_books.sqlite")

        Базовая_визуализация.set_background_image(self)
        Базовая_визуализация.set_font_size(self)

        self.books.clicked.connect(self.click_handling)
        self.authors.clicked.connect(self.click_handling)
        self.genres.clicked.connect(self.click_handling)
        self.returne.clicked.connect(self.close)

    def click_handling(self):
        button_name = self.sender().objectName()
        if button_name == "books":
            file_path = self.select_folder("books-scv")

            data = self.connection.cursor().execute("SELECT * FROM books").fetchall()

            if data:
                with open(file_path, 'w', newline='', encoding="utf8") as csvfile:
                    writer = csv.writer(
                        csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow(['no', 'where', 'who', 'following', 'control'])
                    for row in data:
                        words_in_row = row.split(', ')
                        if words_in_row[0] not in yet:
                            writer.writerow([cnt, words_in_row[1], words_in_row[0], words_in_row[2],
                                             len(words_in_row[1] + words_in_row[0] + words_in_row[2])])
                            cnt += 1
                        yet.append(words_in_row[0])
        if button_name == "authors":
            subprocess.run([sys.executable, 'Окно_для_добавления_книги.py'])
        if button_name == "genres":
            subprocess.run([sys.executable, 'Окно_для_просмотра_авторов.py'])
        else:
            subprocess.run([sys.executable, 'Окно_для_просмотра_жанров_книг.py'])




def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())