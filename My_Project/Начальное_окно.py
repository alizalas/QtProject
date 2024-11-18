
import sys

from PyQt6 import uic
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('first_window.ui', self)
        # Устанавливаем фоновое изображение для всего окна
        self.set_background_image("image.png")

    def set_background_image(self, image_path):
        # Загружаем изображение
        pixmap = QPixmap(image_path)
        # Устанавливаем стиль для QMainWindow с фоновым изображением
        style_sheet = f"""
                QMainWindow {{
                    background-image: url({image_path});
                    background-repeat: no-repeat;
                    background-position: center;
                    background-attachment: fixed;
                    background-size: cover;
                }}
                """
        self.setStyleSheet(style_sheet)

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())