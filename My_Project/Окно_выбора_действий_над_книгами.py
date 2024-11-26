import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow

import subprocess


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('select_action_for_books.ui', self)
        self.search.clicked.connect(self.click_handling)
        self.add.clicked.connect(self.click_handling)
        self.changeInfo.clicked.connect(self.click_handling)
        self.delet.clicked.connect(self.click_handling)

    def click_handling(self):
        button_name = self.sender().objectName()
        if button_name == "search":
            subprocess.run([sys.executable, 'Окно_для_поиска_книг.py'])
        elif button_name == "add":
            subprocess.run([sys.executable, 'Окно_для_добавления_книг.py'])
        elif button_name == "changeInfo":
            subprocess.run([sys.executable, 'Окно_для_изменения_книг.py'])
        else:
            subprocess.run([sys.executable, 'Окно_для_удаления_книг.py'])


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())