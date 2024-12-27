import csv
import json
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QFont, QDesktopServices
from PyQt6.QtWidgets import QWidget, QMessageBox, QTableWidgetItem, QPushButton, QCompleter, QFileDialog
import datetime

from My_Project import Window_manager, Window_for_adding_an_item, Window_for_changing_film, Window_for_changing_book


def set_font_size(self):
    with open("Constants.json", 'r') as file:
        data = json.load(file)

    new_font = QFont(self.font())
    new_font.setPointSize(data["font"])
    self.setFont(new_font)
    for widget in self.findChildren(QWidget):
        widget.setFont(new_font)


def set_font_color(self):
    with open("Constants.json", 'r') as file:
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
    with open("Constants.json", 'r') as file:
        data = json.load(file)

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
    Менеджер_окон.open_next_window(Окно_добавления_значения.MyWidget)

    with open("Constants.json", 'r') as file:
        data = json.load(file)["signalText"]

    self.genre.addItems([str(data)])
    self.connection.cursor().execute(f"INSERT INTO genres(genre) VALUES('{data}')")
    self.connection.commit()


def realisation_with_additional_features(self, res, headers, col_num):
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
                    i, j, QTableWidgetItem(str(elem) if elem and elem != 'NULL' else ''))

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.cellClicked.connect(self.open_link)
    else:
        self.statusBar().setStyleSheet("background-color: white; color: red;")
        self.statusBar().showMessage('Ничего не нашлось', 3000)
        QMessageBox.question(self, '', "Ничего не нашлось")


def open_link(self, row, col):
    if col == self.tableWidget.columnCount() - 3:
        item = self.tableWidget.item(row, col)
        if item:
            link = LinkItem(item.text())
            QDesktopServices.openUrl(QUrl(link.link))


def edit_row(self, num, col_num):
    row_values = [self.tableWidget.item(num, col).text() for col in range(col_num)]
    modify_variable_in_file({"change": row_values})

    if len(row_values) == 8:
        Менеджер_окон.open_next_window(Окно_для_изменения_фильма.MyWidget)
    else:
        Менеджер_окон.open_next_window(Окно_для_изменения_книги.MyWidget)


def delete_row(self, num, col_num):
    row_values = [self.tableWidget.item(num, col).text() for col in range(col_num)]

    if len(row_values) == 8:
        valid = QMessageBox.question(
            self, '', "Действительно удалить <i>фильм с параметрами:</i>" + '<p>' + '<br>'.join(
                [f"<b>название:</b> {row_values[1]}", f"<b>режиссёр:</b> {row_values[2]}",
                 f"<b>год:</b> {row_values[3]}",
                 f"<b>жанр:</b> {row_values[4]}", f"<b>продолжительность:</b> {row_values[5]}",
                 f"<b>рейтинг:</b> {row_values[6]}", f"<b>ссылка:</b> {row_values[7]}?"]),
            buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if valid == QMessageBox.StandardButton.Yes:
            self.tableWidget.removeRow(num)
            self.connection.cursor().execute("DELETE FROM films WHERE id = ?", (row_values[0],))
            self.connection.commit()
    else:
        valid = QMessageBox.question(
            self, '', "Действительно удалить <i>книгу с параметрами:</i>" + '<p>' + '<br>'.join(
                [f"<b>название:</b> {row_values[1]}", f"<b>автор:</b> {row_values[2]}", f"<b>год:</b> {row_values[3]}",
                 f"<b>жанр:</b> {row_values[4]}", f"<b>ссылка:</b> {row_values[5]}?"]),
            buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if valid == QMessageBox.StandardButton.Yes:
            self.tableWidget.removeRow(num)
            self.connection.cursor().execute("DELETE FROM books WHERE id = ?", (row_values[0],))
            self.connection.commit()


def simple_realisation(self, res, headers, col_num):
    if res:
        self.tableWidget.setColumnCount(col_num)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(headers)

        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)

            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem) if elem and elem != 'NULL' else ''))

        self.tableWidget.resizeColumnsToContents()
    else:
        self.statusBar().setStyleSheet("background-color: white; color: red;")
        self.statusBar().showMessage('Ничего не нашлось', 3000)
        QMessageBox.question(self, '', "Ничего не нашлось")


def select_folder(self, file_name):
    folder_path = QFileDialog.getExistingDirectory(self, 'Выберите папку', options=QFileDialog.Option.ShowDirsOnly)

    if folder_path:
        file_path = f"{folder_path}/{file_name}({datetime.datetime.now().strftime('%d-%m-%Y_%H-%M')}).csv"
        return file_path


def make_csv(self, file_path, data, headers):
    if data:
        with open(file_path, 'w', newline='', encoding="utf8") as csvfile:
            writer = csv.writer(
                csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(headers)
            for row in data:
                writer.writerow(list(row))

        QMessageBox.question(self, '',
                             f"Данные из выбранной Вами таблицы <b>успешно сохранены</b> по <i>пути</i>:<p>{file_path}")
    else:
        QMessageBox.question(self, '', "В выбранной Вами таблице <b>нет данных</b>")
    self.go_back()


def modify_variable_in_file(new_value):
    with open("Constants.json", 'r') as file:
        data = json.load(file)

    data.update(new_value)

    with open("Constants.json", 'w') as file:
        json.dump(data, file, indent=4)


def set_compliter(self, table):
    completer = QCompleter([el[0] for el in self.connection.cursor().execute(f"SELECT name FROM {table}").fetchall()],
                           self)
    completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
    completer.setFilterMode(Qt.MatchFlag.MatchContains)
    return completer


class LinkItem(QTableWidgetItem):
    def __init__(self, link):
        super().__init__()
        self.link = link

    def data(self, role):
        if role == Qt.ItemDataRole.DisplayRole:
            return f'<a href="{self.link}"></a>'
        return super().data(role)
