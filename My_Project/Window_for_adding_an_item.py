import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow
from My_Project import Basic_visualization, Window_manager


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('add_item.ui', self)

        Базовая_визуализация.set_background_image(self)
        Базовая_визуализация.set_font_size(self)

        self.set.clicked.connect(self.set_item)
        self.returne.clicked.connect(self.go_back)

    def set_item(self):
        Базовая_визуализация.modify_variable_in_file({"signalText": self.lineEdit.text()})
        self.go_back()

    def go_back(self):
        Менеджер_окон.close_window(MyWidget)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
