import subprocess
import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('first_window.ui', self)
        # Устанавливаем фоновое изображение для всего окна
        self.set_background_image("image5.png")
        self.books.clicked.connect(self.open_next_window)
        self.films.clicked.connect(self.open_next_window)
        self.reference.clicked.connect(self.open_next_window)

    def set_background_image(self, image_path):
        # Устанавливаем стиль для QMainWindow с фоновым изображением
        style_sheet = f"""
                QMainWindow {{
                    background-image: url({image_path});
                    background-repeat: no-repeat;
                    background-position: center;
                    background-attachment: fixed;
                    background-size: contain;
                }}
                """
        self.setStyleSheet(style_sheet)

    def open_next_window(self):
        button_name = self.sender().objectName()
        if button_name == "books":
            subprocess.run([sys.executable, 'Окно_выбора_действий_над_книгами.py'])
        elif button_name == "films":
            subprocess.run([sys.executable, 'Окно_выбора_действий_над_фильмами.py'])
        elif button_name == "reference":
            subprocess.run([sys.executable, 'Окно_справки.py'])

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())