from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel

BOTTOM_BAR_BUTTON_STYLE = """
    QPushButton {
        background-color: #4f46e5;
        color: white;
        border-radius: 6px;
        padding: 4px 12px;
        font-size: 14px;
    }

    QPushButton:hover {
        background-color: #4338ca;
    }

    QPushButton:disabled {
        background-color: #e5e7eb;
        color: #9ca3af;
    }
"""

class ExpenseBottomBar(QWidget):
    def __init__(self,handle_previous_page,handle_next_page):
        super().__init__()
        self.handle_previous_page = handle_previous_page
        self.handle_next_page = handle_next_page
        self.create_expense_bottom_bar()

    def create_expense_bottom_bar(self):

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 8, 0, 0)
        layout.setSpacing(12)
        self.setLayout(layout)

        self.expense_result_label = QLabel("No records loaded")
        self.expense_result_label.setStyleSheet("""
            color: #475569;
            font-size: 16px;
        """)

        self.prev_page_button = QPushButton("Previous")
        self.prev_page_button.setFixedHeight(32)
        self.prev_page_button.setStyleSheet(BOTTOM_BAR_BUTTON_STYLE)
        self.prev_page_button.setCursor(Qt.CursorShape.PointingHandCursor)


        self.next_page_button = QPushButton("  Next  ")
        self.next_page_button.setFixedHeight(32)
        self.next_page_button.setStyleSheet(BOTTOM_BAR_BUTTON_STYLE)
        self.next_page_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.prev_page_button.clicked.connect(self.handle_previous_page)
        self.next_page_button.clicked.connect(self.handle_next_page)

        layout.addWidget(self.expense_result_label)
        layout.addStretch()
        layout.addWidget(self.prev_page_button)
        layout.addWidget(self.next_page_button)

