import json
import sqlite3
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow



class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('change2_book.ui', self)
        self.connection = sqlite3.connect("My_books.sqlite")
        with open("Константы.json", 'r') as file:
            data = json.load(file)
        self.title.setText(data["changeBook"][1])
        self.author.setText(data["changeBook"][2])
        self.year.setText(data["changeBook"][3])
        # self.genre.setEditable(True)
        # self.genre.setCurrentText(data["changeBook"][4])
        spisok = [''] + [el[0] for el in self.connection.cursor().execute("SELECT genre FROM genres").fetchall()]
        self.genre.addItems(spisok)
        self.genre.setCurrentIndex(spisok.index(data["changeBook"][4]))
        self.save.clicked.connect(self.click_handling)

    def click_handling(self):
        pass


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())