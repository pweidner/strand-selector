from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

from strand_selector.io.autosave import save_session
from strand_selector.io.exporter import (
    export_annotations,
    export_selected,
)

from strand_selector.gui.pdf_viewer import PDFViewer


class MainWindow(QMainWindow):

    def __init__(
        self,
        session,
        pdf_loader,
    ):
        super().__init__()

        self.session = session
        self.pdf_loader = pdf_loader

        self.history = []

        self.setWindowTitle(
            "Strand Selector"
        )

        self.info_label = QLabel()

        self.viewer = PDFViewer()

        layout = QVBoxLayout()

        layout.addWidget(
            self.info_label,
            stretch=0,
        )

        layout.addWidget(
            self.viewer,
            stretch=1,
        )

        widget = QWidget()

        widget.setLayout(layout)

        self.setCentralWidget(widget)

        self.update_display()

    def update_display(self):

        idx = self.session.current_index

        cell_info = (
            self.pdf_loader
            .get_cell_info(idx)
        )

        pixmap = (
            self.pdf_loader
            .render_page(idx)
        )

        self.viewer.show_pixmap(
            pixmap
        )

        self.info_label.setText(
            f"Cell: {cell_info['cell_id']}    "
            f"Reads: {cell_info['reads']}    "
            f"DupRate: {cell_info['duplicate_rate']}    "
            f"Cell {idx+1}/{self.session.total_cells}"
        )

    def annotate(self, label):

        idx = self.session.current_index

        cell_info = (
            self.pdf_loader
            .get_cell_info(idx)
        )

        cell_id = (
            cell_info["cell_id"]
        )

        self.history.append(
            (
                idx,
                cell_id,
            )
        )

        self.session.annotations[
            cell_id
        ] = label

        self.session.current_index += 1

        save_session(
            self.session,
            self.session.output_dir
            / "autosave.json",
        )

        if (
            self.session.current_index
            >= self.session.total_cells
        ):

            export_annotations(
                self.session,
		self.session.output_dir,
            )

            export_selected(
                self.session,
		self.session.output_dir,
            )

            self.close()
            return

        self.update_display()

    def undo(self):

        if not self.history:
            return

        idx, cell_id = (
            self.history.pop()
        )

        self.session.current_index = idx

        self.session.annotations.pop(
            cell_id,
            None,
        )

        self.update_display()

    def keyPressEvent(
        self,
        event,
    ):

        key = event.key()

        if key == Qt.Key_Right:
            self.annotate(
                "selected"
            )

        elif key == Qt.Key_Down:
            self.annotate(
                "low_reads"
            )

        elif key == Qt.Key_U:
            self.annotate(
                "brdu_under"
            )

        elif key == Qt.Key_O:
            self.annotate(
                "brdu_over"
            )

        elif key == Qt.Key_S:
            self.annotate(
                "spikey"
            )

        elif key == Qt.Key_Backspace:
            self.undo()
