from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFrame


class ClickableFrame(QFrame):

    clicked = Signal()

    def mousePressEvent(self, event):
        self.clicked.emit()
        event.accept()