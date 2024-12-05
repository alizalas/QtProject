import subprocess
import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow
import Базовая_визуализация

#
# from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QLineEdit, QPushButton, QVBoxLayout
# from PyQt6.QtCore import Qt
#
# class MyWidget(QWidget):
#     def init(self):
#         super().init()
#         self.initUI()
#
#     def initUI(self):
#         self.setWindowTitle("Пример с Tooltip PyQt")
#
#         label = QLabel("Наведите на меня!")
#         label.setToolTip("Это подсказка для метки.")
#
#         entry = QLineEdit()
#         entry.setToolTip("Введите ваше имя здесь.")
#
#
#         button = QPushButton("Кнопка")
#         button.setToolTip("Нажмите для выполнения действия.")
#
#         layout = QVBoxLayout()
#         layout.addWidget(label)
#         layout.addWidget(entry)
#         layout.addWidget(button)
#
#         self.setLayout(layout)
#
#
# if name == 'main':
#     app = QApplication([])
#     window = MyWidget()
#     window.show()
#     app.exec()

class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('first_window.ui', self)
        self.setWindowTitle("Начальное_окно")
        self.reference.setToolTip("Введите ваше имя здесь.")
        self.settings.setToolTip("Введите ваше имя здесь.")
        self.exit.setToolTip("Введите ваше имя здесь.")
        self.reference.setToolTip("Введите ваше имя здесь.")
        Базовая_визуализация.set_background_image(self)
        Базовая_визуализация.set_font(self)
        self.books.clicked.connect(self.open_next_window)
        self.films.clicked.connect(self.open_next_window)
        self.reference.clicked.connect(self.open_next_window)
        self.settings.clicked.connect(self.open_next_window)
        self.exit.clicked.connect(self.open_next_window)


    def open_next_window(self):
        button_name = self.sender().objectName()
        if button_name == "books":
            subprocess.run([sys.executable, 'Окно_выбора_действий_над_книгами.py'])
        elif button_name == "films":
            subprocess.run([sys.executable, 'Окно_выбора_действий_над_фильмами.py'])
        elif button_name == "reference":
            subprocess.run([sys.executable, 'Окно_справки.py'])
        elif button_name == "settings":
            subprocess.run([sys.executable, 'Окно_настроек.py'])
        else:
            self.close()

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())