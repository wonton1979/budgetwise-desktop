from PySide6.QtCore import QEvent, QPoint, QTimer, Qt
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QDateEdit


class PopupDateEdit(QDateEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setCalendarPopup(True)

        line_edit = self.lineEdit()
        if line_edit is not None:
            line_edit.setReadOnly(True)
            line_edit.installEventFilter(self)

    def eventFilter(self, watched, event):
        if (
            watched is self.lineEdit()
            and event.type() == QEvent.Type.MouseButtonPress
            and event.button() == Qt.MouseButton.LeftButton
        ):
            self.setFocus()

            QTimer.singleShot(300, self._open_calendar)

            return True

        return super().eventFilter(watched, event)

    def _open_calendar(self) -> None:
        arrow_position = QPoint(
            self.width() - 12,
            self.height() // 2,
        )

        QTest.mouseClick(
            self,
            Qt.MouseButton.LeftButton,
            Qt.KeyboardModifier.NoModifier,
            arrow_position,
        )