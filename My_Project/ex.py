# import sys
# from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton,
#                              QVBoxLayout, QHBoxLayout, QSizePolicy)
# from PyQt6.QtCore import Qt
#
# class AdaptiveWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.initUI()
#
#     def initUI(self):
#         # Создаем основной макет
#         main_layout = QVBoxLayout()
#
#         # Создаем виджеты
#         label = QLabel("Введите текст:")
#         input_field = QLineEdit()
#         button = QPushButton("Нажми меня")
#
#         # Настройка политики размера для виджетов
#         input_field.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
#         button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
#
#         # Создаем горизонтальный макет для кнопки
#         button_layout = QHBoxLayout()
#         button_layout.addStretch(1)  # Добавляем растягивающийся элемент
#         button_layout.addWidget(button)
#         button_layout.addStretch(1)  # Еще один растягивающийся элемент
#
#         # Добавляем виджеты в основной макет
#         main_layout.addWidget(label)
#         main_layout.addWidget(input_field)
#         main_layout.addLayout(button_layout)
#
#         # Устанавливаем макет для окна
#         self.setLayout(main_layout)
#
#         # Настройки окна
#         self.setWindowTitle('Адаптивное окно')
#         self.setGeometry(100, 100, 300, 200)
#         self.show()
#
#     def resizeEvent(self, event):
#         # При изменении размера окна, обновляем макет
#         self.layout().activate()
#         super().resizeEvent(event)
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = AdaptiveWindow()
#     sys.exit(app.exec())
# from PyQt6.QtWidgets import QFileDialog
#
#
# #
# # import sqlite3
# #
# # con = sqlite3.connect("My_books.sqlite")
# #
# # cur = con.cursor()
# #
# # result = cur.execute("select id from authors where name = 'Достоевский Ф.М.'").fetchall()[0][0]
# #
# # print(result)
# #
# # con.close()
# # author ="sdfgsdfg"
# # spisok = list(map(str,list(range(14))))
# # print(f'INSERT INTO authors(name) VALUES("{author}") and name in ("' + '","'.join(spisok) + '")')
#
#
# #
# # from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QWidget
# # from PyQt6.QtCore import Qt
# #
# # class MainWindow(QMainWindow):
# #     def __init__(self):
# #         super().__init__()
# #
# #         self.table = QTableWidget()
# #         self.table.setColumnCount(5)  # 5 колонок: данные + редактировать + удалить
# #         self.table.setHorizontalHeaderLabels(["Название", "Год", "Режиссер", " ", " "])
# #         self.table.setRowCount(0) # Начальное количество строк 0
# #
# #
# #         layout = QVBoxLayout()
# #         layout.addWidget(self.table)
# #         central_widget = QWidget()
# #         central_widget.setLayout(layout)
# #         self.setCentralWidget(central_widget)
# #
# #         self.add_film("Фильм 1", 2020, "Режиссер 1")
# #         self.add_film("Фильм 2", 2021, "Режиссер 2")
# #         self.add_film("Фильм 3", 2022, "Режиссер 3")
# #
# #
# #
# #     def add_film(self, title, year, director):
# #         row = self.table.rowCount()
# #         self.table.insertRow(row)
# #
# #         self.table.setItem(row, 0, QTableWidgetItem(title))
# #         self.table.setItem(row, 1, QTableWidgetItem(str(year)))
# #         self.table.setItem(row, 2, QTableWidgetItem(director))
# #
# #         edit_button = QPushButton("Редактировать")
# #         edit_button.clicked.connect(lambda checked, row=row: self.edit_film(row)) # Передача номера строки через лямбда-функцию
# #         self.table.setCellWidget(row, 3, edit_button)
# #
# #         delete_button = QPushButton("Удалить")
# #         delete_button.clicked.connect(lambda checked, row=row: self.delete_film(row)) # Передача номера строки через лямбда-функцию
# #         self.table.setCellWidget(row, 4, delete_button)
# #
# #         self.table.resizeColumnsToContents() # Автоматически подгоняет размер колонок
# #
# #
# #     def edit_film(self, row):
# #         print(f"Редактирование фильма в строке {row}")
# #         # Здесь реализуйте логику редактирования фильма
# #         # Например, откройте диалоговое окно для редактирования данных
# #
# #     def delete_film(self, row):
# #         print(f"Удаление фильма в строке {row}")
# #         self.table.removeRow(row)
# #         # Здесь реализуйте логику удаления фильма
# #
# #
# #
# # app = QApplication([])
# # window = MainWindow()
# # window.show()
# # app.exec()
#
# #
# # import sys
# # from PyQt6.QtWidgets import (QApplication, QWidget, QLineEdit, QCompleter,
# #                              QVBoxLayout)
# # from PyQt6.QtCore import Qt
# #
# #
# # class AutocompleteLineEdit(QLineEdit):
# #     def __init__(self, suggestions):
# #         super().__init__()
# #         self.completer = QCompleter(suggestions, self)
# #         self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
# #         self.completer.setFilterMode(Qt.MatchFlag.MatchContains)  # Поиск совпадений по вхождению
# #         self.setCompleter(self.completer)
# #
# #
# # class MainWindow(QWidget):
# #     def __init__(self):
# #         super().__init__()
# #         self.setGeometry(300, 300, 300, 300)
# #         self.setWindowTitle('Автодополнение в PyQt6')
# #
# #         layout = QVBoxLayout()
# #
# #         # Список вариантов для автодополнения
# #         suggestions = ["apple", "banana", "apricot", "avocado", "cherry", "grapefruit", "grape", "kiwi", "lemon",
# #                        "lime", "mango", "melon", "orange", "peach", "pear", "pineapple", "plum", "raspberry",
# #                        "strawberry", "tomato"]
# #
# #         # Создаем поле ввода с автодополнением
# #         self.input_field = AutocompleteLineEdit(suggestions)
# #         layout.addWidget(self.input_field)
# #
# #         self.setLayout(layout)
# #
# #
# # if __name__ == '__main__':
# #     app = QApplication(sys.argv)
# #     window = MainWindow()
# #     window.show()
# #     sys.exit(app.exec())
#
# from PyQt6.QtCore import QProcess
#
# # Запуск нового окна
# процесс = QProcess()
# процесс.start(sys.executable, ['следующий_файл.py'])

import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QMainWindow
from PyQt6.QtCore import QUrl

class LinkItem(QTableWidgetItem):
    def __init__(self, link):
        super().__init__()
        self.link = link

    def data(self, role):
        if role == Qt.ItemDataRole.DisplayRole:
            return f'<a href="{self.link}"></a>'
        return super().data(role)

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.table = QTableWidget()
        self.table.setRowCount(1)
        self.table.setColumnCount(2)

        self.table.setItem(0, 0, QTableWidgetItem('Текст'))
        self.table.setItem(0, 1, QTableWidgetItem('https://www.google.com'))

        self.table.cellClicked.connect(self.open_link)

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

    def open_link(self, row, col):
        if col == 1:
            item = self.table.item(row, col)
            link = LinkItem(item.text())
            QDesktopServices.openUrl(QUrl(link.link))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())