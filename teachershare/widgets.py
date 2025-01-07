from typing import Callable

from PyQt5.QtWidgets import QWidget, QComboBox, QLabel, QPushButton, QTextEdit
from PyQt5.QtCore import Qt



def create_combo(window: QWidget, elements: list, on_select: Callable) -> QWidget:
    """Create combo box from elements and register a callback function."""
    combo = QComboBox(window,)
    for elem in elements:
        combo.addItem(elem)
    combo.currentTextChanged.connect(on_select)
    return combo


def create_label(window: QWidget, caption: str) -> QWidget:
    """Create label from caption."""
    label = QLabel(caption, window)
    label.setAlignment(Qt.AlignCenter)
    label.setStyleSheet("border: 2px solid black; padding: 20px;")
    return label


def create_button(window: QWidget, caption: str, on_click: Callable) -> QWidget:
    """Create button from caption and register a callback function."""
    button = QPushButton(caption, window)
    button.clicked.connect(on_click)
    return button


def create_log(window: QWidget) -> QWidget:
    """Create read-only text field."""
    log = QTextEdit(window)
    log.setReadOnly(True)
    log.setFixedHeight(150)
    return log
