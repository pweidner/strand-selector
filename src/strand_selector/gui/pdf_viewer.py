from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt


class PDFViewer(QLabel):

    def __init__(self):

        super().__init__()

        self.setAlignment(Qt.AlignCenter)

        self.original_pixmap = None

    def show_pixmap(self, pixmap):

        self.original_pixmap = pixmap

        self._rescale()

    def resizeEvent(self, event):

        super().resizeEvent(event)

        self._rescale()

    def _rescale(self):

        if self.original_pixmap is None:
            return

        scaled = self.original_pixmap.scaled(
            self.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )

        self.setPixmap(scaled)
