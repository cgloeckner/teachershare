import sys

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout

from .widgets import *


class Gui:
    def __init__(self, window: QWidget, student_homes: dict) -> None:
        # setup combo box with class names
        self.class_names = list(student_homes.keys())
        self.class_combo = create_combo(window, self.class_names, self.on_class_select)
        self.class_name = self.class_combo.currentText

        # setup drag and drop area for files & dirs
        self.drag_box_caption = "Dateien und Ordner per Drag & Drop hier ablegen"
        self.drag_label = create_label(window, self.drag_box_caption)
        self.drag_files = []

        # setup share button
        self.share_button = create_button(window, "Teilen", self.on_share_click)

        # setup log box
        self.log_box = create_log(window)

        # register drag and drop
        window.setAcceptDrops(True)
        window.dragEnterEvent = self.on_drag_enter
        window.dropEvent = self.on_drag_drop

        # create layout
        layout = QVBoxLayout()
        layout.addWidget(self.class_combo)
        layout.addWidget(self.drag_label)
        layout.addWidget(self.share_button)
        layout.addWidget(self.log_box)
        window.setLayout(layout)

    def on_class_select(self, class_name: str) -> None:
        """React on selecting a class."""
        self.class_name = class_name

    def on_drag_enter(self, event) -> None:
        """Only accept files being dragged in."""
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
    
    def on_drag_drop(self, event) -> None:
        """Store filenames for later."""
        self.drag_files = event.mimeData().urls()
        self.drag_label.setText(self.drag_box_caption)

        if not self.drag_files:
            return

        # display dropped filenames
        file_paths = "\n".join([file.toLocalFile() for file in self.drag_files])
        self.drag_label.setText(f"{file_paths}")

    def on_share_click(self) -> None:
        """React on click to share"""
        print('FIXME: send files to selected class\' students and add a useful log message')


def run(student_homes: dict) -> None: 
    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle("Dateien und Ordner teilen")
    window.setGeometry(100, 100, 800, 600)

    Gui(window, student_homes)

    window.show()
    sys.exit(app.exec_())
