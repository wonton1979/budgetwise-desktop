from pathlib import Path

from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import QDialog, QVBoxLayout, QFrame, QLabel, QHBoxLayout, QPushButton, QSizePolicy

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


class MessageDialog(QDialog):
    def __init__(self,message_title,message_content,handle_delete=False):
        super().__init__()
        self.display_name = None
        self.expense_id = None
        self.setWindowTitle(message_title)
        self.setModal(True)
        self.message_content = message_content
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(8, 8, 8, 8)
        self.setLayout(self.main_layout)
        self.confirm_delete = None

    def information_dialog(self):

        self.information_dialog = QFrame()
        self.information_dialog.setStyleSheet("""
                    background-color: white;
                    border-radius: 10px;
                """)

        message_label_layout = QHBoxLayout()
        message_label_layout.setContentsMargins(10,10,10,10)
        message_label_layout.setSpacing(10)

        message_type_icon = QSvgWidget(f"{BASE_DIR}/icons/warning_message_icon.svg")
        message_type_icon.setFixedSize(32, 32)

        message_content_label = QLabel(self.message_content)
        message_content_label.setStyleSheet("color: #4f46e5;font-size: 12px; font-weight: 600;")

        message_label_layout.addWidget(message_type_icon)
        message_label_layout.addWidget(message_content_label)

        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(10,10,10,15)

        ok_button = QPushButton("OK")
        ok_button.setFixedHeight(28)
        ok_button.setFixedWidth(100)
        ok_button.setStyleSheet("""
                            QPushButton {
                                background-color: #4f46e5;
                                color: white;
                                border-radius: 8px;
                                font-size: 14px;
                                font-weight: 600;
                            }
                            QPushButton:hover {
                                background-color: #4338ca;
                            }
                        """)

        button_layout.addStretch()

        button_layout.addWidget(ok_button)

        button_layout.addStretch()

        self.main_layout.addLayout(message_label_layout)
        self.main_layout.addLayout(button_layout)

        ok_button.clicked.connect(self.reject)

    def error_dialog(self):

        self.error_dialog = QFrame()
        self.error_dialog.setStyleSheet("""
                    background-color: white;
                    border-radius: 10px;
                """)

        message_label_layout = QHBoxLayout()
        message_label_layout.setContentsMargins(10,10,10,10)
        message_label_layout.setSpacing(10)

        message_type_icon = QSvgWidget(f"{BASE_DIR}/icons/error_message_icon.svg")
        message_type_icon.setFixedSize(32, 32)

        message_content_label = QLabel(self.message_content)
        message_content_label.setStyleSheet("color: #4f46e5;font-size: 12px; font-weight: 600;")

        message_label_layout.addWidget(message_type_icon)
        message_label_layout.addWidget(message_content_label)

        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(10,10,10,15)

        ok_button = QPushButton("OK")
        ok_button.setFixedHeight(28)
        ok_button.setFixedWidth(100)
        ok_button.setStyleSheet("""
                            QPushButton {
                                background-color: #4f46e5;
                                color: white;
                                border-radius: 8px;
                                font-size: 14px;
                                font-weight: 600;
                            }
                            QPushButton:hover {
                                background-color: #4338ca;
                            }
                        """)

        button_layout.addStretch()

        button_layout.addWidget(ok_button)

        button_layout.addStretch()

        self.main_layout.addLayout(message_label_layout)
        self.main_layout.addLayout(button_layout)

        ok_button.clicked.connect(self.reject)






