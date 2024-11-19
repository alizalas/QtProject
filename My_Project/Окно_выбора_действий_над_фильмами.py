import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow

import subprocess


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('select_action_for_films.ui', self)
        self.search.clicked.connect(self.click_handling)
        self.add.clicked.connect(self.click_handling)
        self.addInfo.clicked.connect(self.click_handling)

    def click_handling(self):
        button_name = self.sender().objectName()
        if button_name == "search":
            # Запускаем второй файл и завершаем текущий процесс
            subprocess.run([sys.executable, 'Окно_для_поиска_фильмов.py'])
        elif button_name == "add":
            pass
        else:
            pass


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())