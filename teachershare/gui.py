import sys
import pathlib
import time

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout

from .widgets import *
from .dirs import copy_element


class Gui:
    def __init__(self, window: QWidget, student_homes: dict) -> None:
        self.source_paths = []
        self.student_homes = student_homes

        # setup combo box with class names
        self.class_combo = create_combo(window, list(student_homes.keys()), self.on_class_select)

        # setup drag and drop area for files & dirs
        self.drag_box_caption = "Dateien und Ordner per Drag & Drop hier ablegen"
        self.drag_label = create_label(window, self.drag_box_caption)

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
        pass

    def on_drag_enter(self, event) -> None:
        """Only accept files being dragged in."""
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
    
    def on_drag_drop(self, event) -> None:
        """Store filenames for later."""
        dropped_files = event.mimeData().urls()
        self.drag_label.setText(self.drag_box_caption)

        if not dropped_files:
            return

        # create pathlib objects
        self.source_paths = [pathlib.Path(elem.toLocalFile()) for elem in dropped_files]

        # display filenames
        filename_list = '\n'.join([f'{elem}' for elem in self.source_paths])
        self.drag_label.setText(f'{filename_list}')

    def on_share_click(self) -> None:
        """React on click to share"""
        self.log_box.setText('')
        class_name = str(self.class_combo.currentText())

        start_time = time.time()
        for src_path in self.source_paths:
            self.log_box.append(f'Austeilen von {src_path}')
            
            for dst_dir in self.student_homes[class_name]:
                self.log_box.append(f'\tan {dst_dir}')
                copy_element(src_path, dst_dir)
        
        elapsed = time.time() - start_time
        self.log_box.append(f'Abgeschlossen in {elapsed:.2f}s')


def run(student_homes: dict) -> None: 
    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle("Dateien und Ordner teilen")
    window.setGeometry(100, 100, 800, 600)

    Gui(window, student_homes)

    window.show()
    sys.exit(app.exec_())
