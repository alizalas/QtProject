import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow

import Базовая_визуализация


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('add_item.ui', self)

        Базовая_визуализация.set_background_image(self)
        Базовая_визуализация.set_font_size(self)

        self.set.clicked.connect(self.set_item)

    def set_item(self):
        Базовая_визуализация.modify_variable_in_file({"signalText": self.lineEdit.text()})
        self.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())