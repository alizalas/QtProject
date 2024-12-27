import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow
import Window_manager
import Basic_visualization


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('../design/reference.ui', self)

        Basic_visualization.set_background_image(self)
        Basic_visualization.set_font_size(self)

        self.setWindowTitle("Окно справки")
        self.returne.setToolTip("Закрыть окно")

        self.returne.clicked.connect(self.go_back)

    def go_back(self):
        Window_manager.close_window(MyWidget)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
