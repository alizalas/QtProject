import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow
import Basic_visualization, Window_manager, Window_for_selecting_actions_on_books, \
    Window_for_selecting_actions_on_films, Reference_window, Settings_window, Window_for_selecting_actions_on_books_csv, \
    Window_for_selecting_actions_on_films_csv


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('first_window.ui', self)

        Basic_visualization.set_background_image(self)
        Basic_visualization.set_font_size(self)

        self.setWindowTitle("Начальное окно")
        self.books.setToolTip("Здесь можно работать с каталогом <b>книг</b>")
        self.films.setToolTip("Здесь можно работать с каталогом <b>фильмов</b>")
        self.reference.setToolTip(
            "Здесь можно больше узнать о нашем <b>приложении</b> и том, как с ним <b>работать</b>")
        self.settings.setToolTip("Здесь можно <b>изменить настройки</b> окон")
        self.exit.setToolTip("<b>Выйти</b> из приложения")
        self.books_scv.setToolTip("Здесь можно импортировать данные из каталога <b>книг</b>")
        self.films_scv.setToolTip("Здесь можно импортировать данные из каталога <b>фильмов</b>")

        self.books.clicked.connect(self.open_next_window)
        self.films.clicked.connect(self.open_next_window)
        self.reference.clicked.connect(self.open_next_window)
        self.settings.clicked.connect(self.open_next_window)
        self.exit.clicked.connect(self.exit_the_application)
        self.books_scv.clicked.connect(self.open_next_window)
        self.films_scv.clicked.connect(self.open_next_window)

        self._allow_close = False
        Window_manager.save_window(MyWidget, self)

    def open_next_window(self):
        button_name = self.sender().objectName()
        if button_name == "books":
            Window_manager.open_next_window(Window_for_selecting_actions_on_books.MyWidget)
        elif button_name == "films":
            Window_manager.open_next_window(Window_for_selecting_actions_on_films.MyWidget)
        elif button_name == "reference":
            Window_manager.open_next_window(Reference_window.MyWidget)
        elif button_name == "settings":
            Window_manager.open_next_window(Settings_window.MyWidget)
        elif button_name == "books_scv":
            Window_manager.open_next_window(Window_for_selecting_actions_on_books_csv.MyWidget)
        else:
            Window_manager.open_next_window(Window_for_selecting_actions_on_films_csv.MyWidget)

    def exit_the_application(self):
        self._allow_close = True
        Window_manager.close_all_windows()

    def closeEvent(self, event):
        if self._allow_close:
            event.accept()
        else:
            event.ignore()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
