_windows = {}


def save_window(window_class, window_instance):
    """
    Сохраняет окно в словаре.
    """

    global _windows
    _windows[window_class] = window_instance


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


def close_window(window_class):
    """
        Закрывает выбранное окно.
    """

    global _windows

    if window_class in _windows.keys():
        window = _windows[window_class]
        window.close()
        del _windows[window_class]


def close_all_windows():
    """
    Закрывает все открытые окна.
    """

    global _windows
    for window in list(_windows.keys()):
        close_window(window)
