import json
import subprocess
import sys

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QMessageBox, QTableWidgetItem, QPushButton


def set_font(self):
    with open("Константы.json", 'r') as file:
        data = json.load(file)
    new_font = QFont(self.font())
    new_font.setPointSize(data["font"])
    self.setFont(new_font)
    for widget in self.findChildren(QWidget):
        widget.setFont(new_font)

def set_background_image(self):
    with open("Константы.json", 'r') as file:
        data = json.load(file)
    style_sheet = f"""
            QMainWindow {{
                background-image: url({data["background_picture"]});
                background-repeat: no-repeat;
                background-position: center;
                background-attachment: fixed;
                background-size: contain;
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
                lambda checked, num: edit(self, num, col_num))  # Передача номера строки через лямбда-функцию
            self.tableWidget.setCellWidget(num, col_num, edit)

            delete = QPushButton("Удалить")
            delete.clicked.connect(
                lambda checked, num: delete(self, num, col_num))  # Передача номера строки через лямбда-функцию
            self.tableWidget.setCellWidget(num, col_num + 1, delete)

            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

        self.tableWidget.resizeColumnsToContents()
    else:
        self.statusBar().showMessage('Ничего не нашлось')

def edit(self, num, col_num):
    print(f"Редактирование в строке {num}")
    row_values = [self.tableWidget.item(num, col).text() for col in range(col_num)]
    modify_variable_in_file("Константы.json", {"change": row_values})
    subprocess.run([sys.executable, 'Окно_для_изменения_книги.py'])

def delete(self, num, col_num):
    print(f"Удаление фильма в строке {num}")
    row_values = [self.tableWidget.item(num, col).text() for col in range(col_num)]
    valid = QMessageBox.question(
        self, '', "Действительно удалить элемент с такими параметрами: " + ", ".join(row_values),
        buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    if valid == QMessageBox.StandardButton.Yes:
        self.tableWidget.removeRow(num)
        self.connection.cursor().execute("DELETE FROM films WHERE id = ?", (row_values[0], ))
        self.connection.commit()

def modify_variable_in_file(new_value):
    # Чтение JSON-файла
    with open("Константы.json", 'r') as file:
        data = json.load(file)

    data.update(new_value)

    with open("Константы.json", 'w') as file:
        json.dump(data, file, indent=4)