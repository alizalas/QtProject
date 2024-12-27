import sqlite3
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
import Window_manager
import Basic_visualization


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('../design/select_action_for_films-csv.ui', self)

        Basic_visualization.set_background_image(self)
        Basic_visualization.set_font_size(self)

        self.connection = sqlite3.connect("../databases/My_films.sqlite")

        self.choice.clicked.connect(self.choice_folder)
        self.returne.clicked.connect(self.go_back)

    def choice_folder(self):
        if self.films.isChecked():
            file_path = Basic_visualization.select_folder(self, "films-csv")
            data = self.connection.cursor().execute("SELECT * FROM films").fetchall()
            headers = ['id', 'название', 'режиссёр', 'год', 'жанр', 'продолжительность', 'рейтинг']
            Basic_visualization.make_csv(self, file_path, data, headers)

        elif self.directors.isChecked():
            file_path = Basic_visualization.select_folder(self, "directors-csv")
            data = self.connection.cursor().execute("SELECT * FROM directors").fetchall()
            headers = ['id', 'режиссёр']
            Basic_visualization.make_csv(self, file_path, data, headers)

        elif self.genres.isChecked():
            file_path = Basic_visualization.select_folder(self, "genres-csv")
            data = self.connection.cursor().execute("SELECT * FROM genres").fetchall()
            headers = ['id', 'жанр']
            Basic_visualization.make_csv(self, file_path, data, headers)

        else:
            QMessageBox.question(self, '', "Вы <b>не выбрали таблицу</b>, из которой хотите импортитовать данные")

    def go_back(self):
        Window_manager.close_window(MyWidget)

    def closeEvent(self, event):
        self.connection.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
