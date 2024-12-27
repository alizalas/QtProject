import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow
import Basic_visualization, Window_manager, Window_for_searching_books, Window_for_adding_a_book, \
    Window_for_viewing_authors, Window_for_viewing_genres


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('select_action_for_books.ui', self)

        Basic_visualization.set_background_image(self)
        Basic_visualization.set_font_size(self)

        self.search.clicked.connect(self.click_handling)
        self.add.clicked.connect(self.click_handling)
        self.listAuthors.clicked.connect(self.click_handling)
        self.listGenres.clicked.connect(self.click_handling)
        self.returne.clicked.connect(self.click_handling)

    def click_handling(self):
        button_name = self.sender().objectName()
        if button_name == "search":
            Window_manager.open_next_window(Window_for_searching_books.MyWidget)
        elif button_name == "add":
            Window_manager.open_next_window(Window_for_adding_a_book.MyWidget)
        elif button_name == "listAuthors":
            Window_manager.open_next_window(Window_for_viewing_authors.MyWidget)
        elif button_name == "listGenres":
            Basic_visualization.modify_variable_in_file({"database": "books"})
            Window_manager.open_next_window(Window_for_viewing_genres.MyWidget)
        else:
            Window_manager.close_window(MyWidget)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
