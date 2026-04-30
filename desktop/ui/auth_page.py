from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFrame, QLineEdit,
    QPushButton, QStackedWidget
)


class AuthPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        page_layout = QVBoxLayout()
        page_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(page_layout)

        self.setStyleSheet("background-color: #0f172a;")

        self.card = QFrame()
        self.card.setFixedWidth(420)
        self.card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 14px;
            }
        """)

        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(32, 32, 32, 32)
        card_layout.setSpacing(14)
        self.card.setLayout(card_layout)

        title = QLabel("Budget Wise")
        title.setStyleSheet("""
            color: #0f172a;
            font-size: 26px;
            font-weight: 700;
        """)

        subtitle = QLabel("Sign in to manage your family budget")
        subtitle.setStyleSheet("""
            color: #64748b;
            font-size: 13px;
        """)

        self.auth_stack = QStackedWidget()

        card_layout.addWidget(title)
        card_layout.addWidget(subtitle)
        card_layout.addSpacing(12)
        card_layout.addWidget(self.auth_stack)

        page_layout.addStretch()
        page_layout.addWidget(self.card)
        page_layout.addStretch()

        self.login_form = self.create_login_form()
        self.auth_stack.addWidget(self.login_form)

        self.register_form = self.create_register_form()
        self.auth_stack.addWidget(self.register_form)

        self.show_login_form()

    def create_login_form(self):
        form = QWidget()
        form.setStyleSheet("background: transparent;")
        layout = QVBoxLayout()
        layout.setSpacing(10)
        form.setLayout(layout)

        email_label = QLabel("Email")
        email_label.setStyleSheet("color: #334155; font-size: 13px;")

        self.login_email_input = QLineEdit()
        self.login_email_input.setPlaceholderText("Enter your email")
        self.login_email_input.setFixedHeight(36)
        self.login_email_input.setStyleSheet("""
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 0 10px;
            font-size: 14px;
        """)

        password_label = QLabel("Password")
        password_label.setStyleSheet("color: #334155; font-size: 13px;")

        self.login_password_input = QLineEdit()
        self.login_password_input.setEchoMode(QLineEdit.Password)
        self.login_password_input.setPlaceholderText("Enter your password")
        self.login_password_input.setFixedHeight(36)
        self.login_password_input.setStyleSheet("""
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 0 10px;
            font-size: 14px;
        """)

        self.login_button = QPushButton("Login")
        self.login_button.setFixedHeight(40)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #4f46e5;
                color: white;
                border-radius: 8px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #4338ca;
            }
        """)

        self.switch_to_register = QPushButton("No account? Create one")
        self.switch_to_register.setCursor(Qt.PointingHandCursor)
        self.switch_to_register.setStyleSheet("""
            QPushButton {
                color: #4f46e5;
                font-size: 12px;
                font-weight: 500;
                background: transparent;
                border: none;
                text-align: left;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)

        self.switch_to_register.clicked.connect(self.show_register_form)

        layout.addWidget(email_label)
        layout.addWidget(self.login_email_input)
        layout.addWidget(password_label)
        layout.addWidget(self.login_password_input)
        layout.addSpacing(8)
        layout.addWidget(self.login_button)
        layout.addSpacing(10)
        layout.addWidget(self.switch_to_register)
        layout.addStretch()

        return form

    def create_register_form(self):
        form = QWidget()
        form.setStyleSheet("background: transparent;")

        layout = QVBoxLayout()
        layout.setSpacing(10)
        form.setLayout(layout)

        name_label = QLabel("Name")
        name_label.setStyleSheet("color: #334155; font-size: 13px; background: transparent;")

        self.register_name_input = QLineEdit()
        self.register_name_input.setPlaceholderText("Enter your name")
        self.register_name_input.setFixedHeight(36)
        self.register_name_input.setStyleSheet(self.get_input_style())

        email_label = QLabel("Email")
        email_label.setStyleSheet("color: #334155; font-size: 13px; background: transparent;")

        self.register_email_input = QLineEdit()
        self.register_email_input.setPlaceholderText("Enter your email")
        self.register_email_input.setFixedHeight(36)
        self.register_email_input.setStyleSheet(self.get_input_style())

        password_label = QLabel("Password")
        password_label.setStyleSheet("color: #334155; font-size: 13px; background: transparent;")

        self.register_password_input = QLineEdit()
        self.register_password_input.setEchoMode(QLineEdit.Password)
        self.register_password_input.setPlaceholderText("Create a password")
        self.register_password_input.setFixedHeight(36)
        self.register_password_input.setStyleSheet(self.get_input_style())

        confirm_label = QLabel("Confirm Password")
        confirm_label.setStyleSheet("color: #334155; font-size: 13px; background: transparent;")

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setPlaceholderText("Confirm your password")
        self.confirm_password_input.setFixedHeight(36)
        self.confirm_password_input.setStyleSheet(self.get_input_style())

        family_code_label = QLabel("Family Code (Optional)")
        family_code_label.setStyleSheet("color: #334155; font-size: 13px; background: transparent;")

        self.family_code_input = QLineEdit()
        self.family_code_input.setPlaceholderText("Enter family code if joining a family")
        self.family_code_input.setFixedHeight(36)
        self.family_code_input.setStyleSheet(self.get_input_style())

        self.register_button = QPushButton("Create Account")
        self.register_button.setFixedHeight(40)
        self.register_button.setStyleSheet(self.get_primary_button_style())

        self.switch_to_login = QPushButton("Already have an account? Login")
        self.switch_to_login.setCursor(Qt.PointingHandCursor)
        self.switch_to_login.setStyleSheet("""
            QPushButton {
                color: #4f46e5;
                font-size: 12px;
                font-weight: 500;
                background: transparent;
                border: none;
                text-align: left;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)

        self.switch_to_login.clicked.connect(self.show_login_form)

        layout.addWidget(name_label)
        layout.addWidget(self.register_name_input)
        layout.addWidget(email_label)
        layout.addWidget(self.register_email_input)
        layout.addWidget(password_label)
        layout.addWidget(self.register_password_input)
        layout.addWidget(confirm_label)
        layout.addWidget(self.confirm_password_input)
        layout.addWidget(family_code_label)
        layout.addWidget(self.family_code_input)
        layout.addSpacing(8)
        layout.addWidget(self.register_button)
        layout.addSpacing(10)
        layout.addWidget(self.switch_to_login)
        layout.addStretch()

        return form

    def show_login_form(self):
        self.auth_stack.setCurrentWidget(self.login_form)
        self.auth_stack.setFixedHeight(260)

    def show_register_form(self):
        self.auth_stack.setCurrentWidget(self.register_form)
        self.auth_stack.setFixedHeight(470)

    def get_input_style(self):
        return """
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 0 10px;
            font-size: 14px;
        """

    def get_primary_button_style(self):
        return """
            QPushButton {
                background-color: #4f46e5;
                color: white;
                border-radius: 8px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #4338ca;
            }
        """

if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    window = AuthPage()
    window.resize(600, 700)
    window.show()

    sys.exit(app.exec())