import json
import sys
from PyQt6 import uic
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsPixmapItem, QGraphicsView, QColorDialog, \
    QMessageBox
import Window_manager
import Basic_visualization


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('../design/settings.ui', self)

        with open("../jsondir/Constants.json", 'r') as file:
            data = json.load(file)

        self.changeFont.setValue(data["font"])
        self.color = data["color"]

        if data["background_picture"] == "image_1.png":
            self.radioButton_1.setChecked(True)
        elif data["background_picture"] == "image_2.png":
            self.radioButton_2.setChecked(True)
        elif data["background_picture"] == "image_3.png":
            self.radioButton_3.setChecked(True)
        elif data["background_picture"] == "image_4.png":
            self.radioButton_4.setChecked(True)
        elif data["background_picture"] == "image_5.png":
            self.radioButton_5.setChecked(True)
        elif data["background_picture"] == "image_6.png":
            self.radioButton_6.setChecked(True)

        self.changeColor.clicked.connect(self.change_color)
        self.save.clicked.connect(self.save_result)
        self.returne.clicked.connect(self.go_back)

        # Создаём QGraphicsScene
        self.scene_1 = QGraphicsScene()
        self.image_1.setScene(self.scene_1)
        self.load_image("../pictures/image_1.png", 1)

        self.scene_2 = QGraphicsScene()
        self.image_2.setScene(self.scene_2)
        self.load_image("../pictures/image_2.png", 2)

        self.scene_3 = QGraphicsScene()
        self.image_3.setScene(self.scene_3)
        self.load_image("../pictures/image_3.png", 3)

        self.scene_4 = QGraphicsScene()
        self.image_4.setScene(self.scene_4)
        self.load_image("../pictures/image_4.png", 4)

        self.scene_5 = QGraphicsScene()
        self.image_5.setScene(self.scene_5)
        self.load_image("../pictures/image_5.png", 5)

        self.scene_6 = QGraphicsScene()
        self.image_6.setScene(self.scene_6)
        self.load_image("../pictures/image_6.png", 6)

        Basic_visualization.set_font_size(self)
        Basic_visualization.set_font_color(self)

        self.setWindowTitle("Окно настроек")
        self.changeColor.setToolTip("Выберите цвет текста в приложении")
        self.changeFont.setToolTip("Выберите размер текста в приложении")
        self.radioButton_1.setToolTip("Выберите изображение для фона приложения")
        self.radioButton_2.setToolTip("Выберите изображение для фона приложения")
        self.radioButton_3.setToolTip("Выберите изображение для фона приложения")
        self.radioButton_4.setToolTip("Выберите изображение для фона приложения")
        self.radioButton_5.setToolTip("Выберите изображение для фона приложения")
        self.radioButton_6.setToolTip("Выберите изображение для фона приложения")
        self.returne.setToolTip("Закрыть окно")

    def load_image(self, image_path, number):
        # Настройка масштабирования (по желанию)
        graphics_view = getattr(self, f'image_{number}')
        graphics_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        graphics_view.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        graphics_view.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        graphics_view.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)

        pixmap = QPixmap(image_path)
        # Создаём QGraphicsPixmapItem и добавляем в сцену
        pixmap_item = QGraphicsPixmapItem(pixmap)
        scene = getattr(self, f'scene_{number}')
        scene.addItem(pixmap_item)

    def change_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color = color.name()
            self.changeColor.setStyleSheet(
                f"QPushButton {{ color: rgb(255, 255, 255); background-color: {color.name()}; }}")

    def save_result(self):
        if self.radioButton_1.isChecked():
            Basic_visualization.modify_variable_in_file({"background_picture": "image_1.png"})
        elif self.radioButton_2.isChecked():
            Basic_visualization.modify_variable_in_file({"background_picture": "image_2.png"})
        elif self.radioButton_3.isChecked():
            Basic_visualization.modify_variable_in_file({"background_picture": "image_3.png"})
        elif self.radioButton_4.isChecked():
            Basic_visualization.modify_variable_in_file({"background_picture": "image_4.png"})
        elif self.radioButton_5.isChecked():
            Basic_visualization.modify_variable_in_file({"background_picture": "image_5.png"})
        elif self.radioButton_6.isChecked():
            Basic_visualization.modify_variable_in_file({"background_picture": "image_6.png"})

        Basic_visualization.modify_variable_in_file({"font": self.changeFont.value()})
        Basic_visualization.modify_variable_in_file({"color": self.color})

        Basic_visualization.set_font_size(self)
        Basic_visualization.set_font_color(self)

        QMessageBox.question(
            self, '', "Перезапустите приложение, чтобы все изменения <b>отобразились корректно</b>")

        self.go_back()

    def go_back(self):
        Window_manager.close_window(MyWidget)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
