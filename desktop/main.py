import datetime
import sys

import requests

from services.auth_service import get_current_user_profile
from services.dashboard_service import get_dashboard_data, get_spending_chart_data, \
    get_monthly_category_expenses_chart_data
from ui.auth_page import AuthPage

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon, QFontDatabase, QFont
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, QPushButton,
                               QVBoxLayout, QLabel, QFrame, QStackedWidget, QMessageBox)
from pathlib import Path

from ui.dashboard.dashboard_page import DashboardPage
from ui.expenses.expenses_page import ExpensesPage
from ui.profile.profile_dialog import ProfileDialog
from ui.recurring_expenses.recurring_expense_page import RecurringExpensePage
from utils.uk_date_format import uk_date_format

BASE_DIR = Path(__file__).resolve().parent
CURRENT_DATE = datetime.datetime.today()
CURRENT_MONTH_NAME = CURRENT_DATE.strftime("%B")
CURRENT_MONTH_INTEGER = CURRENT_DATE.strftime("%m")
CURRENT_YEAR = CURRENT_DATE.strftime("%Y")


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.token_type = None
        self.access_token = None
        self.setWindowTitle("Budget Wise Desktop")
        self.resize(1200, 780)
        self.setup_main_container()


    def setup_main_container(self):
        self.app_stack = QStackedWidget()
        self.setCentralWidget(self.app_stack)
        self.app_stack.setStyleSheet("background-color: #020617;")

        self.auth_page = AuthPage(on_login_success=self.handle_login_success)

        self.main_app_page = QWidget()
        self.main_app_page.setStyleSheet("background-color: #0f172a;")

        main_layout = QHBoxLayout()
        self.main_app_page.setLayout(main_layout)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(16)

        self.setup_sidebar()
        self.setup_main_area()

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.main_area)

        self.app_stack.addWidget(self.auth_page)
        self.app_stack.addWidget(self.main_app_page)

        self.app_stack.setCurrentWidget(self.auth_page)

    def setup_sidebar(self):
        self.sidebar = QFrame()
        self.sidebar_buttons = []
        self.sidebar.setFixedWidth(220)
        self.sidebar.setStyleSheet("""
                   QFrame {
                       background-color: #ffffff;
                       border-radius: 10px;
                   }
               """)
        sidebar_layout = QVBoxLayout()
        self.sidebar.setLayout(sidebar_layout)
        sidebar_layout.setContentsMargins(18, 24, 18, 24)
        sidebar_layout.setSpacing(12)
        app_name = QLabel("Budget Wise")
        app_name.setStyleSheet("""
                   color: black;
                   font-size: 20px;
                   font-weight: 700;
                   margin-bottom: 20px;
               """)

        sidebar_layout.addWidget(app_name)

        dashboard_item = self.create_sidebar_button("Dashboard")
        self.set_button_icon(dashboard_item, "house.png")
        dashboard_item.setStyleSheet("""
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
        dashboard_item.clicked.connect(
            lambda: (
                self.set_active_button(dashboard_item),
                self.content_stack.setCurrentWidget(self.dashboard_page),
                self.load_dashboard_data()
            )
        )

        expenses_item = self.create_sidebar_button("Expenses")
        self.set_button_icon(expenses_item, "credit-card.png")
        expenses_item.clicked.connect(
            lambda: (
                self.set_active_button(expenses_item),
                self.content_stack.setCurrentWidget(self.expenses_page),
                self.expenses_page.handle_load_expenses(),
                self.expenses_page.handle_load_family_expenses()
            )
        )

        income_item = self.create_sidebar_button("Income")
        self.set_button_icon(income_item, "pound-sterling.png")
        income_item.clicked.connect(
            lambda: self.set_active_button(income_item)
        )

        recurring_item = self.create_sidebar_button("Recurring Bills")
        self.set_button_icon(recurring_item, "recurring.png")
        recurring_item.clicked.connect(
            lambda: (
                self.set_active_button(recurring_item),
                self.content_stack.setCurrentWidget(self.recurring_expense_page),
                self.recurring_expense_page.populate_tree()
            )
        )

        savings_item = self.create_sidebar_button("Savings")
        self.set_button_icon(savings_item, "piggy-bank.png")
        savings_item.clicked.connect(
            lambda: self.set_active_button(savings_item)
        )

        health_item = self.create_sidebar_button("Health")
        self.set_button_icon(health_item, "cross.png")
        health_item.clicked.connect(
            lambda: self.set_active_button(health_item)
        )

        appointments_item = self.create_sidebar_button("Appointments")
        self.set_button_icon(appointments_item, "appointment.png")
        appointments_item.clicked.connect(
            lambda: self.set_active_button(appointments_item)
        )

        family_item = self.create_sidebar_button("Family")
        self.set_button_icon(family_item, "family.png")
        family_item.clicked.connect(
            lambda: self.set_active_button(family_item)
        )

        settings_item = self.create_sidebar_button("Settings")
        self.set_button_icon(settings_item, "settings.png")
        settings_item.clicked.connect(
            lambda: self.set_active_button(settings_item)
        )

        sidebar_layout.addWidget(dashboard_item)
        for item in [
            expenses_item,
            income_item,
            recurring_item,
            savings_item,
            health_item,
            appointments_item,
            family_item,
            settings_item,
        ]:
            sidebar_layout.addWidget(item)

        sidebar_layout.addStretch()

        self.sidebar_buttons.extend([
            dashboard_item,
            expenses_item,
            income_item,
            recurring_item,
            savings_item,
            health_item,
            appointments_item,
            family_item,
            settings_item,
        ])

    def setup_main_area(self):
        self.main_area = QFrame()
        self.main_area.setStyleSheet("""
                   background-color: #243447;
                   border-radius: 10px;
                   border: 1px solid rgba(255,255,255,0.06);
               """)
        main_area_layout = QVBoxLayout()

        self.main_area.setLayout(main_area_layout)

        main_area_layout.setContentsMargins(0, 0, 0, 0)
        main_area_layout.setSpacing(16)

        self.create_top_bar()
        main_area_layout.addWidget(self.top_bar, 0)

        self.content_stack = QStackedWidget()

        self.dashboard_page = DashboardPage()

        self.recurring_expense_page = RecurringExpensePage(access_token_getter=self.get_access_token)

        self.content_stack.addWidget(self.dashboard_page)

        self.content_stack.addWidget(self.recurring_expense_page)

        self.expenses_page = ExpensesPage(access_token_getter=self.get_access_token)

        self.content_stack.addWidget(self.expenses_page)

        main_area_layout.addWidget(self.content_stack, 1)


    def create_top_bar(self):
        self.top_bar = QFrame()
        self.top_bar.setFixedHeight(70)
        self.top_bar.setStyleSheet("""
                           QFrame {
                               background-color: #f9fafb;
                               border-radius: 10px;
                           }
                       """)

        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(24, 12, 24, 12)
        self.top_bar.setLayout(top_layout)

        self.top_title = QLabel("Dashboard")
        self.top_title.setStyleSheet("""
                                   font-size: 20px;
                                   font-weight: 600;
                                   color: #1e293b;
                               """)


        self.current_month_year_label = QLabel(f"{CURRENT_MONTH_NAME} {CURRENT_YEAR}")
        self.current_month_year_label.setStyleSheet("""
            color: #475569;
            font-size: 18px;
            font-weight: 600;
            letter-spacing: 1px;
        """)

        self.previous_month_button = QPushButton("      <      ")
        self.previous_month_button .setCursor(Qt.CursorShape.PointingHandCursor)
        self.previous_month_button.setFixedSize(32, 32)

        self.previous_month_button.setStyleSheet("""
                    QPushButton {
                        background-color: #f9fafb;
                        color: #4f46e5;
                        border: none;
                        border-radius: 18px;
                        font-size: 16px;
                        font-weight: 700;
                    }
                    
                    QPushButton:hover {
                        font-size: 26px;
                        font-weight: 900;
                    }
                """)

        self.next_month_button = QPushButton("      >      ")
        self.next_month_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.next_month_button.setFixedSize(32, 32)

        self.next_month_button.setStyleSheet("""
                            QPushButton {
                                background-color: #f9fafb;
                                color: #4f46e5;
                                border: none;
                                border-radius: 18px;
                                font-size: 16px;
                                font-weight: 700;
                            }
                            
                            QPushButton:hover {
                                font-size: 26px;
                                font-weight: 900;
                            }
                        """)

        self.user_profile_button = QPushButton()
        self.user_profile_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.user_profile_button.setStyleSheet("""
            QPushButton {
                padding: 10px;
                font-size: 14px;
                color: #374151;
                background-color: #f3f4f6;
                padding: 8px 14px;
                border-radius: 8px;
                border: none;
                text-align: center;
            }

            QPushButton:hover {
                background-color: #e5e7eb;
            }
        """)

        self.previous_month_button.setFixedSize(40, 40)
        self.next_month_button.setFixedSize(40, 40)
        self.user_profile_button.clicked.connect(self.handle_show_profile_dialog)

        center_month_layout = QHBoxLayout()
        center_month_layout.setSpacing(12)

        center_month_layout.addWidget(self.previous_month_button)
        center_month_layout.addWidget(self.current_month_year_label)
        center_month_layout.addWidget(self.next_month_button)

        top_layout.addWidget(self.top_title)
        top_layout.addStretch()
        top_layout.addLayout(center_month_layout)
        top_layout.addStretch()
        top_layout.addWidget(self.user_profile_button)



    def set_active_button(self, active_button):
        normal_style = """
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
        """

        active_style = """
            QPushButton {
                color: #4f46e5;
                text-align: left;
                padding: 10px 18px;
                border-radius: 10px;
                background-color: #eef2ff;
                border: none;
                font-weight: 600;
            }
        """

        for button in self.sidebar_buttons:
            button.setStyleSheet(normal_style)

        active_button.setStyleSheet(active_style)
        self.top_title.setText(active_button.text().strip())


    def set_button_icon(self, button,icon_name):
        icon_path = BASE_DIR / "icons" / icon_name
        button.setIcon(QIcon(str(icon_path)))
        button.setIconSize(QSize(18, 18))

    def create_sidebar_button(self,text):
        btn = QPushButton("   " + text)
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


    def handle_login_success(self, auth_data):
        self.access_token = auth_data["access_token"]
        self.token_type = auth_data["token_type"]
        username = get_current_user_profile(self.access_token)["data"]["username"]
        self.user_profile_button.setText(username)
        self.app_stack.setCurrentWidget(self.main_app_page)
        self.load_dashboard_data()


    def get_access_token(self):
        return self.access_token

    def handle_show_profile_dialog(self):
        current_user_info = get_current_user_profile(self.access_token)["data"]
        display_name = current_user_info["display_name"]
        email = current_user_info["email"]
        family_code = current_user_info["family_code"]
        self.profile_dialog = ProfileDialog(display_name,email,family_code,self.get_access_token)
        self.profile_dialog.exec()

    def load_dashboard_data(self):

        try:
            dashboard_data = get_dashboard_data(int(CURRENT_YEAR), int(CURRENT_MONTH_INTEGER), self.get_access_token())

            self.dashboard_page.handle_value_update(self.dashboard_page.expense_card_value_label,
                                                    "£" + str(dashboard_data["total_expenses"]))
            self.dashboard_page.handle_value_update(self.dashboard_page.transaction_count_label_value,
                                                    str(dashboard_data["transaction_count"]))
            self.dashboard_page.handle_value_update(self.dashboard_page.top_category_label_value, dashboard_data[
                "top_category"].title() + f" ( £{str(dashboard_data['top_category_amount'])} )")
            self.dashboard_page.handle_value_update(self.dashboard_page.highest_expense_label_value,
                                                    dashboard_data["highest_expense_shop"] + " - £"
                                                    + str(dashboard_data["highest_expense"]) + " - " + uk_date_format(
                                                        str(dashboard_data["highest_expense_date"])))
            self.dashboard_page.handle_value_update(self.dashboard_page.average_daily_spending_value,
                                                    "£" + str(dashboard_data["average_daily_spending"]))

            monthly_spending_chart_data = get_spending_chart_data(int(CURRENT_YEAR), int(CURRENT_MONTH_INTEGER),
                                                                  self.get_access_token())
            self.dashboard_page.weekly_spending_chart.update_chart(monthly_spending_chart_data)

            category_expenses_chart_data = get_monthly_category_expenses_chart_data(int(CURRENT_YEAR),
                                                                                    int(CURRENT_MONTH_INTEGER),
                                                                                    self.get_access_token())
            self.dashboard_page.category_expenses_chart.update_chart(category_expenses_chart_data)

        except requests.RequestException as error:
            QMessageBox.critical(
                self,
                "Connection Error",
                "Failed to connect to server."
            )

        except Exception as error:
            QMessageBox.critical(
                self,
                "Unexpected Error",
                "Can not load dashboard data."
            )


app = QApplication(sys.argv)
font_id = QFontDatabase.addApplicationFont("fonts/Inter-Regular.ttf")
font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
app.setFont(QFont(font_family, 10))
window = MainWindow()
window.show()
sys.exit(app.exec())