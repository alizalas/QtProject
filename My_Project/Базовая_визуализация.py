import json
import subprocess
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QMessageBox, QTableWidgetItem, QPushButton, QCompleter, QFileDialog
import datetime


def set_font_size(self):
    with open("Константы.json", 'r') as file:
        data = json.load(file)
    new_font = QFont(self.font())
    new_font.setPointSize(data["font"])
    self.setFont(new_font)
    for widget in self.findChildren(QWidget):
        widget.setFont(new_font)


def set_font_color(self):
    with open("Константы.json", 'r') as file:
        data = json.load(file)["color"]

    style_sheet = f"""
        QMainWindow 
        * {{
            color: {data};
        }}
        """
    self.setStyleSheet(style_sheet)
    self.changeColor.setStyleSheet(f"QPushButton {{ color: rgb(255, 255, 255); background-color: {data}; }}")


def set_background_image(self):
    with open("Константы.json", 'r') as file:
        data = json.load(file)
    # style_sheet = f"""
    #         QMainWindow {{
    #             background-image: url({data["background_picture"]});
    #             background-repeat: no-repeat;
    #             background-position: center;
    #             background-attachment: fixed;
    #             background-size: contain;
    #             color: red;
    #         }}
    #         """
    style_sheet = f"""
        QMainWindow {{
            background-image: url({data["background_picture"]});
            background-repeat: no-repeat;
            background-position: center;
            background-attachment: fixed;
            background-size: contain;
        }}
        * {{
            color: {data["color"]};
        }}
        """
    self.setStyleSheet(style_sheet)


def add_item(self):
    subprocess.run([sys.executable, 'Окно_добавления_значения.py'])
    with open("Константы.json", 'r') as file:
        data = json.load(file)
    self.genre.addItems([str(data["signalText"])])
    self.connection.cursor().execute(f"INSERT INTO genres(genre) VALUES('{data['signalText']}')")
    self.connection.commit()


def realisation(self, res, headers, col_num):
    if res:
        self.tableWidget.setColumnCount(col_num + 2)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(headers + ['редактировать', 'удалить'])

        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)

            num = self.tableWidget.rowCount() - 1

            edit = QPushButton("Редактировать", self)
            edit.clicked.connect(
                lambda checked, num=num: edit_row(self, num, col_num))  # Передача номера строки через лямбда-функцию
            self.tableWidget.setCellWidget(num, col_num, edit)

            delete = QPushButton("Удалить")
            delete.clicked.connect(
                lambda checked, num=num: delete_row(self, num, col_num))  # Передача номера строки через лямбда-функцию
            self.tableWidget.setCellWidget(num, col_num + 1, delete)

            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem) if elem else ''))

        self.tableWidget.resizeColumnsToContents()
    else:
        self.statusBar().showMessage('Ничего не нашлось')


def edit_row(self, num, col_num):
    print(f"Редактирование в строке {num}")
    row_values = [self.tableWidget.item(num, col).text() for col in range(col_num)]
    modify_variable_in_file({"change": row_values})
    if len(row_values) == 7:
        subprocess.run([sys.executable, 'Окно_для_изменения_фильма.py'])
    else:
        subprocess.run([sys.executable, 'Окно_для_изменения_книги.py'])


def delete_row(self, num, col_num):
    print(f"Удаление в строке {num}")
    row_values = [self.tableWidget.item(num, col).text() for col in range(col_num)]
    if len(row_values) == 7:
        valid = QMessageBox.question(
            self, '', "Действительно удалить <i>фильм с параметрами:</i>" + '<p>' + '<br>'.join(
                [f"<b>название:</b> {row_values[1]}", f"<b>режиссёр:</b> {row_values[2]}",
                 f"<b>год:</b> {row_values[3]}",
                 f"<b>жанр:</b> {row_values[4]}", f"<b>продолжительность:</b> {row_values[5]}",
                 f"<b>рейтинг:</b> {row_values[6]}?"]),
            buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if valid == QMessageBox.StandardButton.Yes:
            self.tableWidget.removeRow(num)
            self.connection.cursor().execute("DELETE FROM films WHERE id = ?", (row_values[0],))
            self.connection.commit()
    else:
        valid = QMessageBox.question(
            self, '', "Действительно удалить <i>книгу с параметрами:</i>" + '<p>' + '<br>'.join(
                [f"<b>название:</b> {row_values[1]}", f"<b>автор:</b> {row_values[2]}", f"<b>год:</b> {row_values[3]}",
                 f"<b>жанр:</b> {row_values[4]}?"]),
            buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if valid == QMessageBox.StandardButton.Yes:
            self.tableWidget.removeRow(num)
            self.connection.cursor().execute("DELETE FROM books WHERE id = ?", (row_values[0],))
            self.connection.commit()


def select_folder(self, file_name):
    folder_path = QFileDialog.getExistingDirectory(self, 'Выберите папку', options=QFileDialog.Option.ShowDirsOnly)
    if folder_path:
        file_path = f"{folder_path}/{file_name}({datetime.datetime.now().strftime('%d-%m-%Y_%H-%M')}).csv"
        return file_path


def modify_variable_in_file(new_value):
    # Чтение JSON-файла
    with open("Константы.json", 'r') as file:
        data = json.load(file)

    data.update(new_value)

    with open("Константы.json", 'w') as file:
        json.dump(data, file, indent=4)


def set_compliter(self, table):
    completer = QCompleter([el[0] for el in self.connection.cursor().execute(f"SELECT name FROM {table}").fetchall()],
                           self)
    completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
    completer.setFilterMode(Qt.MatchFlag.MatchContains)
    return completer
