import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow
from Окно_для_добавления_книги import signal

import subprocess


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('add_item.ui', self)
        self.set.clicked.connect(self.set_item)
        self.text = ''

    def set_item(self):
        self.text = self.lineEdit.text()
        self.close()

    def closeEvent(self, event):
        self.on_window_close()  # Вызов вашей функции при закрытии
        event.accept()  # Закрытие окна

    def on_window_close(self):
        signal(self.text)

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())