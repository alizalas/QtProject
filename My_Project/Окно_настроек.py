import sys
from PyQt6 import uic
from PyQt6.QtGui import QPixmap, QPainter, QFont
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsPixmapItem, QGraphicsView
import Константы


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('settings.ui', self)
        self.save_changes.clicked.connect(self.save_results)
        self.changeLanguage.addItems(["Русский", "English"])

        # Создаём QGraphicsScene
        self.scene_1 = QGraphicsScene()
        self.image_1.setScene(self.scene_1)
        self.load_image("image_1.png", 1)

        self.scene_2 = QGraphicsScene()
        self.image_2.setScene(self.scene_2)
        self.load_image("image_2.png", 2)

        self.scene_3 = QGraphicsScene()
        self.image_3.setScene(self.scene_3)
        self.load_image("image_3.png", 3)

        self.scene_4 = QGraphicsScene()
        self.image_4.setScene(self.scene_4)
        self.load_image("image_4.png", 4)

        self.scene_5 = QGraphicsScene()
        self.image_5.setScene(self.scene_5)
        self.load_image("image_5.png", 5)

        self.scene_6 = QGraphicsScene()
        self.image_6.setScene(self.scene_6)
        self.load_image("image_6.png", 6)

        self.set_font()

    def load_image(self, image_path, n):
        # Настройка масштабирования (по желанию)
        graphics_view = getattr(self, f'image_{n}')
        graphics_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        graphics_view.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        graphics_view.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        graphics_view.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)

        """Загружает изображение и добавляет его в сцену."""
        pixmap = QPixmap(image_path)
        # Создаём QGraphicsPixmapItem и добавляем в сцену
        pixmap_item = QGraphicsPixmapItem(pixmap)
        scene = getattr(self, f'scene_{n}')
        scene.addItem(pixmap_item)

    def set_font(self):
        new_font = QFont(self.font())
        new_font.setPointSize(Константы.font)
        self.setFont(new_font)

    def save_results(self):
        if self.radioButton_1.isChecked():
            self.modify_variable_in_file("Константы.py", "background_picture", '"image_1.png"')
        elif self.radioButton_2.isChecked():
            self.modify_variable_in_file("Константы.py", "background_picture", '"image_2.png"')
        elif self.radioButton_3.isChecked():
            self.modify_variable_in_file("Константы.py", "background_picture", '"image_3.png"')
        elif self.radioButton_4.isChecked():
            self.modify_variable_in_file("Константы.py", "background_picture", '"image_4.png"')
        elif self.radioButton_5.isChecked():
            self.modify_variable_in_file("Константы.py", "background_picture", '"image_5.png"')
        elif self.radioButton_6.isChecked():
            self.modify_variable_in_file("Константы.py", "background_picture", '"image_6.png"')
        self.modify_variable_in_file("Константы.py", "font", self.changeFont.value())
        self.set_font()

    def modify_variable_in_file(self, filename, variable_name, new_value):
        with open(filename, 'r') as f:
            lines = f.readlines()

        with open(filename, 'w') as f:
            for line in lines:
                if line.startswith(variable_name + ' ='):
                    f.write(f'{variable_name} = {new_value}\n')  # Записываем новую строку с измененным значением
                else:
                    f.write(line)  # Записываем остальные строки без изменений


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())