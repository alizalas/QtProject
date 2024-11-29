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

#
# import sqlite3
#
# con = sqlite3.connect("My_books.sqlite")
#
# cur = con.cursor()
#
# result = cur.execute("select id from authors where name = 'Достоевский Ф.М.'").fetchall()[0][0]
#
# print(result)
#
# con.close()
author ="sdfgsdfg"
spisok = list(map(str,list(range(14))))
print(f'INSERT INTO authors(name) VALUES("{author}") and name in ("' + '","'.join(spisok) + '")')