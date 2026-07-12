from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QLabel,
    QLineEdit,
    QPushButton,
    QApplication,
)

from services.user_service import update_user_profile
from ui.components.create_input_component import CreateInputComponent


class ProfileDialog(QDialog):
    def __init__(self, display_name, email, family_code,get_access_token):
        super().__init__()

        self.setWindowTitle("Profile Settings")
        self.setModal(True)
        self.resize(500, 360)
        self.display_name = display_name
        self.email = email
        self.family_code = family_code
        self.get_access_token = get_access_token
        self.create_profile_setting_ui()

    def create_profile_setting_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        self.profile_card = QFrame()
        self.profile_card.setStyleSheet("""
            QFrame {
                background-color: white;

            }
        """)

        profile_card_layout = QVBoxLayout()
        profile_card_layout.setContentsMargins(24, 24, 24, 24)
        profile_card_layout.setSpacing(14)
        self.profile_card.setLayout(profile_card_layout)

        title = QLabel("Profile Settings")
        title.setStyleSheet("""
            color: #0f172a;
            font-size: 22px;
            font-weight: 700;
        """)

        subtitle = QLabel("Manage how your account appears to family members.")
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet("""
            color: #64748b;
            font-size: 13px;
        """)

        profile_card_layout.addWidget(title)
        profile_card_layout.addWidget(subtitle)
        profile_card_layout.addSpacing(8)

        self.display_name_input = CreateInputComponent(
            profile_card_layout,
            "Display Name",
            "e.g. Jerry, Mum, Dad",
            self.display_name,
        )

        self.email_input = CreateInputComponent(
            profile_card_layout,
            "Email",
            "user@email.com",
            self.email,
            readonly=True
        )

        family_code_label = QLabel("Family Code")
        family_code_label.setStyleSheet("""
            color: #334155;
            font-size: 13px;
            font-weight: 500;
        """)

        profile_card_layout.addWidget(family_code_label)

        family_code_row = QHBoxLayout()
        family_code_row.setSpacing(8)

        self.family_code_input = QLineEdit()
        self.family_code_input.setText(self.family_code)
        self.family_code_input.setReadOnly(True)
        self.family_code_input.setFixedHeight(38)

        self.family_code_input.setStyleSheet("""
            QLineEdit {
                background-color: #f1f5f9;
                color: #64748b;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 0 10px;
                font-size: 14px;
            }
        """)

        self.copy_family_code_button = QPushButton("Copy")
        self.copy_family_code_button.setFixedHeight(38)
        self.copy_family_code_button.setFixedWidth(72)
        self.copy_family_code_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.copy_family_code_button.clicked.connect(self.copy_family_code)

        self.copy_family_code_button.setStyleSheet("""
            QPushButton {
                background-color: #eef2ff;
                color: #4f46e5;
                border: 1px solid #c7d2fe;
                border-radius: 8px;
                font-size: 13px;
                font-weight: 600;
            }

            QPushButton:hover {
                background-color: #e0e7ff;
            }
        """)

        family_code_row.addWidget(self.family_code_input, 1)
        family_code_row.addWidget(self.copy_family_code_button)

        profile_card_layout.addLayout(family_code_row)

        profile_card_layout.addSpacing(12)

        bottom_row = QHBoxLayout()
        self.message_label = QLabel()
        self.message_label.setStyleSheet("""
                        color: #22c55e;
                        font-size: 12px;
                    """)
        self.message_label.setText("                     ")
        bottom_row.addWidget(self.message_label)
        bottom_row.addStretch()

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setFixedHeight(38)
        self.cancel_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #e5e7eb;
                color: #374151;
                border-radius: 8px;
                padding: 0 16px;
                font-size: 14px;
            }

            QPushButton:hover {
                background-color: #d1d5db;
            }
        """)

        self.save_button = QPushButton("Save Changes")
        self.save_button.setFixedHeight(38)
        self.save_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #4f46e5;
                color: white;
                border-radius: 8px;
                padding: 0 18px;
                font-size: 14px;
                font-weight: 600;
            }

            QPushButton:hover {
                background-color: #4338ca;
            }
        """)

        self.cancel_button.clicked.connect(self.reject)
        self.save_button.clicked.connect(self.handle_update_display_name)

        bottom_row.addWidget(self.cancel_button)
        bottom_row.addWidget(self.save_button)

        profile_card_layout.addLayout(bottom_row)

        main_layout.addWidget(self.profile_card)


    def copy_family_code(self):
        QApplication.clipboard().setText(self.family_code)
        self.copy_family_code_button.setText("Copied")
        self.copy_family_code_button.setEnabled(False)
        QTimer.singleShot(2000, self.change_copy_button_text)

    def change_copy_button_text(self):
        self.copy_family_code_button.setText("Copy")
        self.copy_family_code_button.setEnabled(True)

    def handle_update_display_name(self):
        access_token = self.get_access_token()
        payload = {
            "display_name": self.display_name_input.get_input_text()
        }
        update_user_profile(payload, access_token)
        self.message_label.setText("Display name updated successfully")
        QTimer.singleShot(2000, self.close_dialog)

    def close_dialog(self):
        self.message_label.setText("                     ")
        self.reject()
