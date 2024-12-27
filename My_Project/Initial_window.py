import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow
from My_Project import Basic_visualization, Window_manager, Window_for_selecting_actions_on_books, \
    Window_for_selecting_actions_on_films, Reference_window, Settings_window, Window_for_selecting_actions_on_books_csv, \
    Window_for_selecting_actions_on_films_csv


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('first_window.ui', self)

        Базовая_визуализация.set_background_image(self)
        Базовая_визуализация.set_font_size(self)

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
        Менеджер_окон.save_window(MyWidget, self)

    def open_next_window(self):
        button_name = self.sender().objectName()
        if button_name == "books":
            Менеджер_окон.open_next_window(Окно_выбора_действий_над_книгами.MyWidget)
        elif button_name == "films":
            Менеджер_окон.open_next_window(Окно_выбора_действий_над_фильмами.MyWidget)
        elif button_name == "reference":
            Менеджер_окон.open_next_window(Окно_справки.MyWidget)
        elif button_name == "settings":
            Менеджер_окон.open_next_window(Окно_настроек.MyWidget)
        elif button_name == "books_scv":
            Менеджер_окон.open_next_window(Окно_выбора_действий_над_книгами_csv.MyWidget)
        else:
            Менеджер_окон.open_next_window(Окно_выбора_действий_над_фильмами_csv.MyWidget)

    def exit_the_application(self):
        self._allow_close = True
        Менеджер_окон.close_all_windows()

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
