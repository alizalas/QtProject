import json
from PyQt6.QtGui import QFont


def set_font(self):
    with open("Константы.json", 'r') as file:
        data = json.load(file)
    new_font = QFont(self.font())
    new_font.setPointSize(data["font"])
    self.setFont(new_font)


def set_background_image(self):
    # Устанавливаем стиль для QMainWindow с фоновым изображением
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

def modify_variable_in_file(filename, new_value):
    # Чтение JSON-файла
    with open(filename, 'r') as file:
        data = json.load(file)

    # Обновление констант в данных JSON-файла
    data.update(new_value)

    # Запись обновленных данных обратно в JSON-файл
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)