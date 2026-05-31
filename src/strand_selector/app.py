from PySide6.QtWidgets import QApplication

from strand_selector.gui.main_window import MainWindow


def run_app(
    session,
    pdf_loader,
):

    app = QApplication([])

    window = MainWindow(
        session=session,
        pdf_loader=pdf_loader,
    )

    window.showMaximized()

    window.show()

    app.exec()
