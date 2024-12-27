_windows = {}


def save_window(window_class, window_instance):
    """
    Сохраняет окно в словаре.
    """

    global _windows
    _windows[window_class] = window_instance

    #print(f"сохранено окно {window_class}, {_windows}")


def open_next_window(window_class):
    """
    Открывает окно. Если окно свернуто - разворачивает его.
    Если окно не существует - создает новое.
    """

    global _windows
    if window_class not in _windows:
        _windows[window_class] = window_class()
    window = _windows[window_class]

    if window.isMinimized():
        window.showNormal()
    else:
        window.show()

    window.raise_()
    window.activateWindow()

    #print(f"открыл окно {window_class}, {_windows}")


def close_window(window_class):
    """
        Закрывает выбранное окно.
    """

    global _windows

    #print(f"{_windows}")

    if window_class in _windows.keys():
        window = _windows[window_class]
        window.close()
        del _windows[window_class]

        #print(f"удалено {window_class}, {_windows}")
    else:
        pass

        #print(f"упс {window_class}, {_windows}")


def close_all_windows():
    """
    Закрывает все открытые окна.
    """

    global _windows
    for window in list(_windows.keys()):
        close_window(window)

# 1
# class WindowManager:
#     _instance = None
#
#     def __new__(cls):
#         if cls._instance is None:
#             cls._instance = super().__new__(cls)
#             cls._instance._windows = {}
#         return cls._instance
#
#     def save_window(self, window_class, window_instance):
#         self._windows[window_class] = window_instance
#         print(f"Сохранено окно {window_class}, {self._windows}")
#
#     def open_next_window(self, window_class):
#         if window_class not in self._windows:
#             self._windows[window_class] = window_class()
#         window = self._windows[window_class]
#
#         if window.isMinimized():
#             window.showNormal()
#         else:
#             window.show()
#
#         window.raise_()
#         window.activateWindow()
#
#         print(f"Открыто окно {window_class}, {self._windows}")
#
#     def close_window(self, window_class):
#         print("Я тут")
#         print(f"{self._windows}")
#         if window_class in self._windows:
#             window = self._windows[window_class]
#             window.close()
#             del self._windows[window_class]
#             print(f"Удалено {window_class}, {self._windows}")
#         else:
#             print(f"Упс {window_class}, {self._windows}")
#
#     def close_all_windows(self):
#         for window in list(self._windows.keys()):
#             self.close_window(window)
#
# # Глобальный экземпляр для удобства использования
# window_manager = WindowManager()


# 2
# class WindowManager:
#     # Словарь для хранения окон будет общим для всех импортов
#     _windows = {}
#
#     @classmethod
#     def save_window(cls, window_class, window_instance):
#         cls._windows[window_class] = window_instance
#         print(f"сохранено окно {window_class}, {cls._windows}")
#
#     @classmethod
#     def open_next_window(cls, window_class):
#         if window_class not in cls._windows:
#             cls._windows[window_class] = window_class()
#         window = cls._windows[window_class]
#
#         if window.isMinimized():
#             window.showNormal()
#         else:
#             window.show()
#
#         window.raise_()
#         window.activateWindow()
#
#         print(f"открыл окно {window_class}, {cls._windows}")
#
#     @classmethod
#     def close_window(cls, window_class):
#         print("я тут")
#         print(f"{cls._windows}")
#         if window_class in cls._windows:
#             window = cls._windows[window_class]
#             window.close()
#             del cls._windows[window_class]
#             print(f"удалено {window_class}, {cls._windows}")
#         else:
#             print(f"упс {window_class}, {cls._windows}")
#
#     @classmethod
#     def close_all_windows(cls):
#         for window in list(cls._windows.keys()):
#             cls.close_window(window)
#
#     @classmethod
#     def get_window(cls, window_class):
#         return cls._windows.get(window_class)


# 3
# class WindowManager:
#     _windows = {}
#
#     @staticmethod
#     def save_window(window_class, window_instance):
#         """
#         Сохраняет окно в словаре.
#         """
#         WindowManager._windows[window_class] = window_instance
#         print(f"сохранено окно {window_class}, {WindowManager._windows}")
#
#     @staticmethod
#     def open_next_window(window_class):
#         """
#         Открывает окно. Если окно свернуто - разворачивает его.
#         Если окно не существует - создает новое.
#         """
#         if window_class not in WindowManager._windows:
#             WindowManager._windows[window_class] = window_class()
#         window = WindowManager._windows[window_class]
#
#         if window.isMinimized():
#             window.showNormal()
#         else:
#             window.show()
#
#         window.raise_()
#         window.activateWindow()
#
#         print(f"открыл окно {window_class}, {WindowManager._windows}")
#
#     @staticmethod
#     def close_window(window_class):
#         print("я тут")
#         print(f"{WindowManager._windows}")
#         if window_class in WindowManager._windows.keys():
#             window = WindowManager._windows[window_class]
#             window.close()
#             del WindowManager._windows[window_class]
#             print(f"удалено {window_class}, {WindowManager._windows}")
#         else:
#             print(f"упс {window_class}, {WindowManager._windows}")
#
#     @staticmethod
#     def close_all_windows():
#         """
#         Закрывает все открытые окна.
#         """
#         for window in list(WindowManager._windows.keys()):
#             WindowManager.close_window(window)


# class WindowManager:
#     _windows = {}
#
#     @staticmethod
#     def save_window(window_class):
#         if window_class not in WindowManager._windows:
#             WindowManager._windows[window_class] = window_class()
#
#     @staticmethod
#     def open_next_window(window_class):
#         if window_class not in WindowManager._windows or not WindowManager._windows[window_class].isVisible():
#             WindowManager._windows[window_class] = window_class()
#         WindowManager._windows[window_class].show()
#         WindowManager._windows[window_class].raise_()
#         WindowManager._windows[window_class].activateWindow()
#
#     @staticmethod
#     def close_window(window_class):
#         if window_class in WindowManager._windows:
#             window = WindowManager._windows[window_class]
#             if window.isVisible():
#                 window.close()
#             del WindowManager._windows[window_class]
#
#     @staticmethod
#     def close_all_windows():
#         """
#         Закрывает все открытые окна.
#         """
#         for window in list(WindowManager._windows.keys()):
#             WindowManager.close_window(window)
#
#     @staticmethod
#     def is_window_open(self, window_name: str) -> bool:
#         """
#         Проверяет, открыто ли указанное окно.
#
#         :param window_name: Имя окна.
#         :return: True, если окно открыто, иначе False.
#         """
#         return window_name in self.windows and self.windows[window_name].isVisible()


# from typing import Dict, Type, Optional
# from PyQt6.QtWidgets import QMainWindow
#
#
# class WindowManager:
#     def __init__(self):
#         self.windows: Dict[str, QMainWindow] = {}  # Словарь для хранения окон
#
#     def get_window(self, window_class: Type[QMainWindow], window_name: str = None) -> Optional[QMainWindow]:
#         """
#         Возвращает существующее окно или создает новое, если оно еще не существует.
#
#         :param window_class: Класс окна, который нужно открыть.
#         :param window_name: Имя окна (опционально). Если не указано, используется имя класса.
#         :return: Экземпляр окна.
#         """
#         if window_name is None:
#             window_name = window_class.__name__
#
#         if window_name not in self.windows or not self.windows[window_name].isVisible():
#             # Создаем новое окно, если его нет или оно не видимо
#             new_window = window_class()
#             self.windows[window_name] = new_window
#             return new_window
#
#         # Возвращаем существующее окно, если оно уже открыто
#         return self.windows[window_name]
#
#     def close_window(self, window_name: str) -> None:
#         """
#         Закрывает указанное окно.
#
#         :param window_name: Имя окна, которое нужно закрыть.
#         """
#         if window_name in self.windows:
#             window = self.windows[window_name]
#             if window.isVisible():
#                 window.close()
#             del self.windows[window_name]
#
#     def close_all_windows(self) -> None:
#         """
#         Закрывает все открытые окна.
#         """
#         for window_name in list(self.windows.keys()):
#             self.close_window(window_name)
#
#     def is_window_open(self, window_name: str) -> bool:
#         """
#         Проверяет, открыто ли указанное окно.
#
#         :param window_name: Имя окна.
#         :return: True, если окно открыто, иначе False.
#         """
#         return window_name in self.windows and self.windows[window_name].isVisible()
#
#     def show_window(self, window_name: str) -> None:
#         """
#         Показывает указанное окно, если оно существует.
#
#         :param window_name: Имя окна.
#         """
#         if window_name in self.windows:
#             window = self.windows[window_name]
#             if not window.isVisible():
#                 window.show()
#
#     def hide_window(self, window_name: str) -> None:
#         """
#         Скрывает указанное окно, если оно существует.
#
#         :param window_name: Имя окна.
#         """
#         if window_name in self.windows:
#             window = self.windows[window_name]
#             if window.isVisible():
#                 window.hide()