import re

import requests
from PySide6.QtCore import Qt, QSize, QTimer
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFrame, QLineEdit,
    QPushButton, QStackedWidget, QHBoxLayout
)

from pathlib import Path

from services.api_client import ApiConnectionError, ResourceNotFoundError, ServerError, AuthenticationError, ApiError
from services.auth_service import register_user,login_user
from ui.components.dialogs.message_dialog import MessageDialog

BASE_DIR = Path(__file__).resolve().parent.parent
USERNAME_REGEX = "^[A-Za-z\\d]{3,12}$"
EMAIL_REGEX = "^([a-zA-Z0-9.-_]+)@([a-zA-Z0-9_-])+\\.[a-zA-Z]{2,10}(.[a-z]{2,8})?$"
PASSWORD_REGEX = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]{8,20}$"

class AuthPage(QWidget):
    def __init__(self, on_login_success=None):
        super().__init__()
        self.on_login_success = on_login_success
        self.setup_ui()

    def setup_ui(self):
        page_layout = QVBoxLayout()
        page_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(page_layout)

        self.setStyleSheet("background-color: #020617;")

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
        page_layout.addWidget(self.card, alignment=Qt.AlignmentFlag.AlignCenter)
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
        layout.setSpacing(5)
        form.setLayout(layout)

        email_label_group = self.create_group_widget()

        email_label = QLabel("Email")
        email_label.setStyleSheet("color: #334155; font-size: 13px;")

        self.login_email_error = QLabel("")
        self.login_email_error.setStyleSheet("""
                            color: #ef4444;
                            font-size: 12px;
                        """)

        email_label_group.layout().addWidget(email_label)
        email_label_group.layout().addWidget(self.login_email_error)

        self.login_email_input = QLineEdit()
        self.login_email_input.setPlaceholderText("Enter your email")
        self.login_email_input.setFixedHeight(36)
        self.login_email_input.setStyleSheet("""
            QLineEdit {
                background-color: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 0 10px;
                font-size: 14px;
            }
            QLineEdit:focus {
                       border: 1px solid #4f46e5;
                   }
        """)

        password_label_group = self.create_group_widget()

        password_label = QLabel("Password")
        password_label.setStyleSheet("color: #334155; font-size: 13px;")

        self.login_password_error = QLabel("")
        self.login_password_error.setStyleSheet("""
                                    color: #ef4444;
                                    font-size: 12px;
                                """)

        password_label_group.layout().addWidget(password_label)
        password_label_group.layout().addWidget(self.login_password_error)

        password_input_group = self.create_group_widget()

        self.login_password_input = QLineEdit()
        self.login_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.login_password_input.setPlaceholderText("Enter your password")
        self.login_password_input.setFixedHeight(36)
        self.login_password_input.setStyleSheet("""
            QLineEdit {
                background-color: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 0 10px;
                font-size: 14px;
            }
            QLineEdit:focus {
                       border: 1px solid #4f46e5;
                   }
        """)
        self.login_password_input.returnPressed.connect(self.handle_login)

        password_view_login = {"is_view":False}

        self.view_password = self.create_view_password_button()
        self.set_button_icon(self.view_password,"view.png")
        self.view_password.setCursor(Qt.CursorShape.PointingHandCursor)
        self.view_password.setFixedWidth(55)
        self.view_password .setStyleSheet("""
                           QPushButton {
                               color: #4f46e5;
                               text-align: left;
                               padding: 10px 18px;
                               border-radius: 10px;
                               background-color: #eef2ff;
                               border: none;
                               font-weight: 600;
                           }
                           QToolTip {
                                color: #4f46e5; 
                                background-color: white; 
                                border: 1px solid white; 
                                font-weight: 800;
                           }
                       """)
        self.view_password.setToolTip("View Your Password")
        self.view_password.clicked.connect(lambda : self.switch_password_view(password_view_login,
                                                                              self.view_password,
                                                                              self.login_password_input)
                                           )

        password_input_group.layout().addWidget(self.login_password_input)
        password_input_group.layout().addWidget(self.view_password)

        self.login_status_label = QLabel("")
        self.login_status_label.setWordWrap(True)
        self.login_status_label.setStyleSheet("color: #ef4444;font-size: 12px;")

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
        self.login_button.setDefault(True)
        self.login_button.clicked.connect(self.handle_login)

        self.switch_to_register = QPushButton("No account? Create one")
        self.switch_to_register.setCursor(Qt.CursorShape.PointingHandCursor)
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

        layout.addWidget(email_label_group)
        layout.addWidget(self.login_email_input)
        layout.addSpacing(8)
        layout.addWidget(password_label_group)
        layout.addWidget(password_input_group)
        layout.addSpacing(12)
        layout.addWidget(self.login_button)
        layout.addSpacing(10)
        layout.addWidget(self.login_status_label)
        layout.addSpacing(10)
        layout.addWidget(self.switch_to_register)

        return form

    def create_register_form(self):
        form = QWidget()
        form.setStyleSheet("background: transparent;")

        layout = QVBoxLayout()
        layout.setSpacing(3)
        form.setLayout(layout)

        username_label_group = self.create_group_widget()

        username_label = QLabel("Username")
        username_label.setStyleSheet("color: #334155; font-size: 13px; background: transparent;")

        self.username_label_error = QLabel("")
        self.username_label_error.setStyleSheet("""
                                                    color: #ef4444;
                                                    font-size: 12px;
                                                """)

        username_label_group.layout().addWidget(username_label)
        username_label_group.layout().addWidget(self.username_label_error)

        self.register_username_input = QLineEdit()
        self.register_username_input.setPlaceholderText("Enter your username, min 3 characters")
        self.register_username_input.setFixedHeight(36)
        self.register_username_input.setStyleSheet(self.get_input_style())

        email_label_group = self.create_group_widget()

        email_label = QLabel("Email")
        email_label.setStyleSheet("color: #334155; font-size: 13px; background: transparent;")

        self.register_email_error = QLabel("")
        self.register_email_error.setStyleSheet("""
                                            color: #ef4444;
                                            font-size: 12px;
                                        """)

        email_label_group.layout().addWidget(email_label)
        email_label_group.layout().addWidget(self.register_email_error)

        self.register_email_input = QLineEdit()
        self.register_email_input.setPlaceholderText("Enter your email")
        self.register_email_input.setFixedHeight(36)
        self.register_email_input.setStyleSheet(self.get_input_style())

        password_label_group = self.create_group_widget()

        password_label = QLabel("Password")
        password_label.setStyleSheet("color: #334155; font-size: 13px; background: transparent;")

        self.register_password_error = QLabel("")
        self.register_password_error.setStyleSheet("color: #ef4444;font-size: 12px;")

        password_label_group.layout().addWidget(password_label)
        password_label_group.layout().addWidget(self.register_password_error)

        password_input_group = self.create_group_widget()

        self.register_password_input = QLineEdit()
        self.register_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.register_password_input.setPlaceholderText("Create a password")
        self.register_password_input.setFixedHeight(36)
        self.register_password_input.setStyleSheet(self.get_input_style())

        password_view_login = {"is_view":False}
        self.register_view_password = self.create_view_password_button()
        self.set_button_icon(self.register_view_password,"view.png")
        self.register_view_password.setCursor(Qt.CursorShape.PointingHandCursor)
        self.register_view_password.setFixedWidth(55)
        self.register_view_password .setStyleSheet("""
                           QPushButton {
                               color: #4f46e5;
                               text-align: left;
                               padding: 10px 18px;
                               border-radius: 10px;
                               background-color: #eef2ff;
                               border: none;
                               font-weight: 600;
                           }
                       """)
        self.register_view_password.clicked.connect(lambda : self.switch_password_view(password_view_login,
                                                                              self.register_view_password,
                                                                              self.register_password_input))

        password_input_group.layout().addWidget(self.register_password_input)
        password_input_group.layout().addWidget(self.register_view_password)

        confirm_password_label_group = self.create_group_widget()

        register_confirm_password_label = QLabel("Confirm Password")
        register_confirm_password_label.setStyleSheet("color: #334155; font-size: 13px; background: transparent;")

        self.register_confirm_password_error = QLabel("")
        self.register_confirm_password_error.setStyleSheet("color: #ef4444;font-size: 12px;")

        confirm_password_label_group.layout().addWidget(register_confirm_password_label)
        confirm_password_label_group.layout().addWidget(self.register_confirm_password_error)

        confirm_password_input_group = self.create_group_widget()

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password_input.setPlaceholderText("Confirm your password")
        self.confirm_password_input.setFixedHeight(36)
        self.confirm_password_input.setStyleSheet(self.get_input_style())

        confirm_password_view_login = {"is_view": False}
        self.confirm_view_password = self.create_view_password_button()
        self.set_button_icon(self.confirm_view_password, "view.png")
        self.confirm_view_password.setCursor(Qt.CursorShape.PointingHandCursor)
        self.confirm_view_password.setFixedWidth(55)
        self.confirm_view_password.setStyleSheet("""
                                   QPushButton {
                                       color: #4f46e5;
                                       text-align: left;
                                       padding: 10px 18px;
                                       border-radius: 10px;
                                       background-color: #eef2ff;
                                       border: none;
                                       font-weight: 600;
                                   }
                               """)
        self.confirm_view_password.clicked.connect(lambda: self.switch_password_view(confirm_password_view_login,
                                                                                      self.confirm_view_password,
                                                                                      self.confirm_password_input))

        confirm_password_input_group.layout().addWidget(self.confirm_password_input)
        confirm_password_input_group.layout().addWidget(self.confirm_view_password)

        family_code_label = QLabel("Family Code (Optional)")
        family_code_label.setStyleSheet("color: #334155; font-size: 13px; background: transparent;")

        self.family_code_input = QLineEdit()
        self.family_code_input.setPlaceholderText("Enter family code if joining a family")
        self.family_code_input.setFixedHeight(36)
        self.family_code_input.setStyleSheet(self.get_input_style())

        self.password_tips_label = QLabel("Password should between 8 and 20 characters."
                                          "At least one uppercase letter,one lowercase letter,"
                                          "one number and one special character.(@$!%*?&)")
        self.password_tips_label.setWordWrap(True)
        self.password_tips_label.setStyleSheet("""
                                                    color: #4f46e5;
                                                    font-size: 12px;
                                                """)


        self.register_button = QPushButton("Create Account")
        self.register_button.setFixedHeight(40)
        self.register_button.setStyleSheet(self.get_primary_button_style())

        self.register_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.register_button.clicked.connect(self.handle_register)

        self.switch_to_login = QPushButton("Already have an account? Login")
        self.switch_to_login.setCursor(Qt.CursorShape.PointingHandCursor)
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

        layout.addWidget(username_label_group)
        layout.addWidget(self.register_username_input)
        layout.addWidget(email_label_group)
        layout.addWidget(self.register_email_input)
        layout.addWidget(password_label_group)
        layout.addWidget(password_input_group)
        layout.addWidget(confirm_password_label_group)
        layout.addWidget(confirm_password_input_group)
        layout.addWidget(family_code_label)
        layout.addWidget(self.family_code_input)
        layout.addSpacing(8)
        layout.addWidget(self.password_tips_label)
        layout.addSpacing(8)
        layout.addWidget(self.register_button)
        layout.addSpacing(10)
        layout.addWidget(self.switch_to_login)


        return form

    def show_login_form(self):
        self.auth_stack.setCurrentWidget(self.login_form)
        self.auth_stack.setFixedHeight(260)

    def show_register_form(self):
        self.auth_stack.setCurrentWidget(self.register_form)
        self.auth_stack.setFixedHeight(470)

    def get_input_style(self):
        return """
            QLineEdit {
                background-color: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 0 10px;
                font-size: 14px;
            }
            QLineEdit:focus {
                       border: 1px solid #4f46e5;
                   }
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

    def login_validation(self):
        self.login_email_error.setText("")
        self.login_password_error.setText("")
        email = self.login_email_input.text().strip()
        password =self.login_password_input.text().strip()

        if not re.match(EMAIL_REGEX, email):
            self.login_email_error.setText(f"Please Enter A Valid Email Address.")
            return False

        if not re.match(PASSWORD_REGEX, password):
            self.login_password_error.setText(f"Please Enter A Valid Password.")
            return False

        return True

    def register_validation(self):
        self.username_label_error.setText("")
        self.register_email_error.setText("")
        self.register_password_error.setText("")
        self.register_confirm_password_error.setText("")

        username = self.register_username_input.text().strip()
        email = self.register_email_input.text().strip()
        password =self.register_password_input.text().strip()
        confirm_password = self.confirm_password_input.text().strip()

        if not re.match(USERNAME_REGEX, username):
            self.username_label_error.setText(f"Please Enter A Valid Username.")
            return False

        if not re.match(EMAIL_REGEX, email):
            self.register_email_error.setText(f"Please Enter A Valid Email Address.")
            return False

        if not re.match(PASSWORD_REGEX, password):
            self.register_password_error.setText(f"Please Enter A Valid Password.")
            return False

        if not password == confirm_password:
            self.register_confirm_password_error.setText(f"Please make sure both passwords match.")
            return False

        return True



    def create_view_password_button(self):
        btn = QPushButton()
        btn.setStyleSheet("""
            QPushButton {
                color: black;
                text-align: left;
                padding: 10px 18px;
                border-radius: 10px;
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                background-color: #e2e8f0;
            }
        """)

        return btn

    def set_button_icon(self,button, icon_name):
        icon_path = BASE_DIR / "icons" / icon_name
        button.setIcon(QIcon(str(icon_path)))
        button.setIconSize(QSize(18, 18))

    def switch_password_view(self,is_view,view_button,password_input):

        is_view["is_view"] = not is_view["is_view"]
        if is_view["is_view"]:
            self.set_button_icon(view_button, "eye-closed.png")
            password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            view_button.setToolTip("Hide Your Password")
        else:
            self.set_button_icon(view_button, "view.png")
            password_input.setEchoMode(QLineEdit.EchoMode.Password)
            view_button.setToolTip("View Your Password")

    def create_group_widget(self):

        group_widget = QWidget()
        group_widget_layout = QHBoxLayout()
        group_widget_layout.setSpacing(4)
        group_widget_layout.setContentsMargins(0, 0, 0, 0)
        group_widget.setLayout(group_widget_layout)

        return group_widget

    def handle_register(self):
        if not self.register_validation():
            return

        username = self.register_username_input.text().strip()
        email = self.register_email_input.text().strip().lower()
        password = self.register_password_input.text().strip()
        family_code = self.family_code_input.text().strip()

        try:
            register_user(username, email, password, family_code)

            self.password_tips_label.setStyleSheet("""
                color: #22c55e;
                font-size: 16px;
            """)
            self.password_tips_label.setText("Account created successfully. Please log in.")

            QTimer.singleShot(2000, self.show_login_form)


        except requests.ConnectionError:

            connection_error_message_dialog = MessageDialog("Connection Error", "Unable to connect to the server.")

            connection_error_message_dialog.error_dialog()

            connection_error_message_dialog.exec_()


        except requests.Timeout:

            timeout_error_message_dialog = MessageDialog("Connection Error", "The request timed out.")

            timeout_error_message_dialog.error_dialog()

            timeout_error_message_dialog.exec_()


        except Exception as error:

            api_error_message_dialog = MessageDialog("API Error", str(error))

            api_error_message_dialog.error_dialog()

            api_error_message_dialog.exec_()

    def handle_login(self):
        if not self.login_validation():
            return

        email = self.login_email_input.text().strip().lower()
        password = self.login_password_input.text().strip()

        try:
            result = login_user(email, password)

            if self.on_login_success:
                self.on_login_success(result)


        except requests.ConnectionError:

            connection_error_message_dialog = MessageDialog("Connection Error", "Unable to connect to the server.")

            connection_error_message_dialog.error_dialog()

            connection_error_message_dialog.exec_()


        except requests.Timeout:

            timeout_error_message_dialog = MessageDialog("Connection Error", "The request timed out.")

            timeout_error_message_dialog.error_dialog()

            timeout_error_message_dialog.exec_()


        except Exception as error:

            api_error_message_dialog = MessageDialog("API Error", str(error))

            api_error_message_dialog.error_dialog()

            api_error_message_dialog.exec_()
