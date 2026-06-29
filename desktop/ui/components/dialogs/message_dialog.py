from pathlib import Path

from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import QDialog, QVBoxLayout, QFrame, QLabel, QHBoxLayout, QPushButton

from utils.clear_layout import clear_layout

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


class MessageDialog(QDialog):
    def __init__(self,message_title,message_content,handle_logout=None):
        super().__init__()
        self.display_name = None
        self.expense_id = None
        self.handle_logout = handle_logout
        self.setWindowTitle(message_title)
        self.setModal(True)
        self.message_content = message_content
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(8, 8, 8, 8)
        self.setLayout(self.main_layout)
        self.dialog = QFrame()

    def information_dialog(self):
        self.creation_dialog("warning_message_icon")

    def error_dialog(self):
        self.creation_dialog("error_message_icon")

    def success_dialog(self):
        self.creation_dialog("success_message_icon")

    def creation_dialog(self,icon_name):
        self.dialog = QFrame()
        self.dialog.setStyleSheet("""
                            background-color: white;
                            border-radius: 10px;
                        """)

        message_label_layout = QHBoxLayout()
        message_label_layout.setContentsMargins(10, 10, 10, 10)
        message_label_layout.setSpacing(10)

        message_type_icon = QSvgWidget(f"{BASE_DIR}/icons/{icon_name}.svg")
        message_type_icon.setFixedSize(32, 32)

        message_content_label = QLabel(self.message_content)
        message_content_label.setStyleSheet("color: #4f46e5;font-size: 12px; font-weight: 600;")

        message_label_layout.addWidget(message_type_icon)
        message_label_layout.addWidget(message_content_label)

        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(10, 10, 10, 15)

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


    def creation_confirmation_dialog(self):
        clear_layout(self.main_layout)
        self.dialog.setStyleSheet("""
                            background-color: white;
                            border-radius: 10px;
                        """)

        message_label_layout = QHBoxLayout()
        message_label_layout.setContentsMargins(10, 10, 10, 10)
        message_label_layout.setSpacing(10)

        message_type_icon = QSvgWidget(f"{BASE_DIR}/icons/warning_message_icon.svg")
        message_type_icon.setFixedSize(32, 32)

        message_content_label = QLabel(self.message_content)
        message_content_label.setStyleSheet("color: #4f46e5;font-size: 12px; font-weight: 600;")

        message_label_layout.addWidget(message_type_icon)
        message_label_layout.addWidget(message_content_label)

        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(10, 10, 10, 15)

        confirm_button = QPushButton("Confirm")
        confirm_button.setFixedHeight(28)
        confirm_button.setFixedWidth(100)
        confirm_button.setStyleSheet("""
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

        cancel_button = QPushButton("Cancel")
        cancel_button.setFixedHeight(28)
        cancel_button.setFixedWidth(100)
        cancel_button.setStyleSheet("""
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


        button_layout.addWidget(confirm_button)
        button_layout.addWidget(cancel_button)

        self.main_layout.addLayout(message_label_layout)
        self.main_layout.addLayout(button_layout)

        confirm_button.clicked.connect(self.handle_logout)
        cancel_button.clicked.connect(self.reject)








