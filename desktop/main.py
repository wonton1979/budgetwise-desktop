from datetime import datetime
import sys

import requests

from services.auth_service import get_current_user_profile
from services.dashboard_service import get_dashboard_data, get_monthly_spending_chart_data, \
    get_monthly_category_expenses_chart_data

from ui.auth.auth_page import AuthPage

from PySide6.QtCore import QSize, Qt, QDate
from PySide6.QtGui import QIcon, QFontDatabase, QFont
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, QPushButton,
                               QVBoxLayout, QLabel, QFrame, QStackedWidget, QComboBox)

from ui.components.dialogs.message_dialog import MessageDialog
from ui.dashboard.dashboard_page import DashboardPage
from ui.expenses.expenses_page import ExpensesPage
from ui.family.family_expense_page import FamilyExpensesPage
from ui.health.health_page import HealthPage
from ui.appointments.appointments_page import AppointmentsPage
from ui.incomes.incomes_page import IncomesPage
from ui.memorable_days.memorable_day_page import MemorableDayPage
from ui.profile.profile_dialog import ProfileDialog
from ui.recurring_expenses.recurring_expense_page import RecurringExpensePage
from ui.savings.savings_page import SavingsPage
from ui.settings.settings_page import SettingsPage
from utils.clear_layout import clear_layout
from utils.combobox_style import get_combo_style
from utils.date_format_convertor import uk_date_format,long_date_format
from config import get_resource_directory

CURRENT_DATE = datetime.today()
CURRENT_MONTH_NAME = CURRENT_DATE.strftime("%B")
CURRENT_MONTH_INTEGER = CURRENT_DATE.strftime("%m")
CURRENT_YEAR = CURRENT_DATE.strftime("%Y")


def create_sidebar_button(text):
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


def set_button_icon(button, icon_name):
    icon_path = get_resource_directory() / "icons" / icon_name
    button.setIcon(QIcon(str(icon_path)))
    button.setIconSize(QSize(18, 18))


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.currency_symbol = None
        self.token_type = None
        self.access_token = None
        self.setWindowTitle("Budget Wise Desktop")
        self.resize(1200, 780)
        self.current_dashboard_date = QDate.currentDate()
        self.username = None
        self.preferred_currency_display = None
        self.preferred_date_format = None
        self.display_name = None
        self.app_stack = QStackedWidget()
        self.setCentralWidget(self.app_stack)
        self.app_stack.setStyleSheet("background-color: #020617;")

        self.auth_page = AuthPage(on_login_success=self.handle_login_success)

        self.main_app_page = QWidget()
        self.main_app_page.setStyleSheet("background-color: #0f172a;")

        self.main_layout = QHBoxLayout()
        self.main_app_page.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(16, 16, 16, 16)
        self.main_layout.setSpacing(16)
        self.setup_main_container()
        self.health_type = None



    def setup_main_container(self):
        clear_layout(self.main_layout)

        self.setup_sidebar()
        self.setup_main_area()

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.main_area)

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

        dashboard_item = create_sidebar_button("Dashboard")
        set_button_icon(dashboard_item, "house.png")
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

        expenses_item = create_sidebar_button("Expenses")
        set_button_icon(expenses_item, "credit-card.png")
        expenses_item.clicked.connect(
            lambda: (
                self.set_active_button(expenses_item),
                self.content_stack.setCurrentWidget(self.expenses_page),
                self.get_current_user_profile(),
                self.expenses_page.handle_load_expenses(currency_symbol=self.currency_symbol,date_format=self.preferred_date_format),
                self.expenses_page.expense_filter.change_date_format_display(new_date_format=self.preferred_date_format)
            )
        )

        income_item = create_sidebar_button("Income")
        set_button_icon(income_item, "pound-sterling.png")
        income_item.clicked.connect(
            lambda: (
                self.set_active_button(income_item),
                self.content_stack.setCurrentWidget(self.incomes_page),
                self.get_current_user_profile(),
                self.incomes_page.load_incomes_data(self.currency_symbol),
                self.incomes_page.add_income_dialog.set_current_date_format(current_date_format=self.preferred_date_format),
                self.incomes_page.update_date_format(new_date_format=self.preferred_date_format)
            )

        )

        recurring_item = create_sidebar_button("Recurring Bills")
        set_button_icon(recurring_item, "recurring.png")
        recurring_item.clicked.connect(
            lambda: (
                self.set_active_button(recurring_item),
                self.content_stack.setCurrentWidget(self.recurring_expense_page),
                self.get_current_user_profile(),
                self.recurring_expense_page.populate_tree(self.currency_symbol),
                self.recurring_expense_page.add_recurring_expense_dialog.change_date_format_display(new_date_format=self.preferred_date_format),
                self.recurring_expense_page.update_date_format(new_date_format=self.preferred_date_format),
            )
        )

        savings_item = create_sidebar_button("Savings")
        set_button_icon(savings_item, "piggy-bank.png")
        savings_item.clicked.connect(
            lambda: (
                self.set_active_button(savings_item),
                self.content_stack.setCurrentWidget(self.savings_page),
                self.get_current_user_profile(),
                self.savings_page.update_date_format(new_date_format=self.preferred_date_format),
                self.savings_page.load_savings_data(self.currency_symbol),
            )
        )

        health_item = create_sidebar_button("Health")
        set_button_icon(health_item, "cross.png")
        health_item.clicked.connect(
            lambda: (
                self.set_active_button(health_item),
                self.content_stack.setCurrentWidget(self.health_page),
                self.get_current_user_profile(),
                self.health_page.load_health_records(),
                self.health_page.weight_line_chart.update_date_format(new_date_format=self.preferred_date_format),
                self.health_page.blood_pressure_line_chart.update_date_format(new_date_format=self.preferred_date_format),
                self.health_page.blood_sugar_line_chart.update_date_format(new_date_format=self.preferred_date_format),
                self.health_page.period_records_table.update_date_format(new_date_format=self.preferred_date_format),
            )
        )

        appointments_item = create_sidebar_button("Appointments")
        set_button_icon(appointments_item, "appointment.png")
        appointments_item.clicked.connect(
            lambda: (
                self.set_active_button(appointments_item),
                self.content_stack.setCurrentWidget(self.appointments_page),
                self.get_current_user_profile(),
                self.appointments_page.add_appointment_dialog.set_current_date_format(self.preferred_date_format),
                self.appointments_page.load_appointments(new_date_format=self.preferred_date_format)
            )
        )

        memorable_days_item = create_sidebar_button("Memorable Days")
        set_button_icon(memorable_days_item, "calendar.png")
        memorable_days_item.clicked.connect(
            lambda: (
                self.set_active_button(memorable_days_item),
                self.content_stack.setCurrentWidget(self.memorable_days_page),
                self.get_current_user_profile(),
                self.memorable_days_page.update_date_format(new_date_format=self.preferred_date_format),
                self.memorable_days_page.load_memorable_days()
            )
        )

        family_item = create_sidebar_button("Family")
        set_button_icon(family_item, "family.png")
        family_item.clicked.connect(
            lambda: (
                self.set_active_button(family_item),
                self.content_stack.setCurrentWidget(self.family_page),
                self.get_current_user_profile(),
                self.family_page.handle_load_family_expenses(currency_symbol=self.currency_symbol,
                                                             new_date_format=self.preferred_date_format),
                self.family_page.handle_load_recurring_expense(self.currency_symbol),
                self.family_page.family_expenses_tab.family_expense_filter.change_date_format_display(new_date_format=self.preferred_date_format)
            )

        )

        settings_item = create_sidebar_button("Settings")
        set_button_icon(settings_item, "settings.png")
        settings_item.clicked.connect(
            lambda: (
                self.set_active_button(settings_item),
                self.content_stack.setCurrentWidget(self.settings_page),
            )
        )

        logout_item = create_sidebar_button("Logout")
        set_button_icon(logout_item, "logout.png")
        logout_item.clicked.connect(
            lambda: (
                self.set_active_button(logout_item),
                self.confirmation_dialog.creation_confirmation_dialog(),
                self.confirmation_dialog.exec()
            )
        )

        sidebar_layout.addWidget(dashboard_item)
        for item in [
            expenses_item,
            income_item,
            recurring_item,
            savings_item,
            health_item,
            appointments_item,
            memorable_days_item,
            family_item,
            settings_item,
            logout_item,
            settings_item
        ]:
            sidebar_layout.addWidget(item)

        sidebar_layout.addStretch()

        sidebar_layout.addWidget(logout_item)

        self.sidebar_buttons.extend([
            dashboard_item,
            expenses_item,
            income_item,
            recurring_item,
            savings_item,
            health_item,
            appointments_item,
            memorable_days_item,
            family_item,
            settings_item,
            logout_item
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

        self.dashboard_page = DashboardPage(self.currency_symbol)

        self.recurring_expense_page = RecurringExpensePage(access_token_getter=self.get_access_token,
                                                           handle_token_expired = self.handle_token_expired_or_logout,
                                                           currency_symbol=self.currency_symbol,
                                                           date_format=self.preferred_date_format)

        self.expenses_page = ExpensesPage(access_token_getter=self.get_access_token,
                                          handle_token_expired = self.handle_token_expired_or_logout,
                                          currency_symbol=self.currency_symbol,date_format=self.preferred_date_format)

        self.incomes_page = IncomesPage(access_token_getter=self.get_access_token,
                                        handle_token_expired = self.handle_token_expired_or_logout,
                                        currency_symbol=self.currency_symbol,date_format=self.preferred_date_format)

        self.savings_page = SavingsPage(access_token_getter=self.get_access_token,
                                        handle_token_expired = self.handle_token_expired_or_logout,
                                        currency_symbol=self.currency_symbol,
                                        date_format=self.preferred_date_format)

        self.health_page = HealthPage(access_token_getter=self.get_access_token,
                                      handle_token_expired = self.handle_token_expired_or_logout,
                                      date_format=self.preferred_date_format)

        self.appointments_page = AppointmentsPage(access_token_getter=self.get_access_token,
                                                  handle_token_expired = self.handle_token_expired_or_logout,
                                                  date_format=self.preferred_date_format)

        self.memorable_days_page = MemorableDayPage(access_token_getter=self.get_access_token,
                                                    handle_token_expired = self.handle_token_expired_or_logout,
                                                    date_format=self.preferred_date_format)

        self.family_page = FamilyExpensesPage(access_token_getter=self.get_access_token,
                                              handle_token_expired = self.handle_token_expired_or_logout,
                                              currency_symbol=self.currency_symbol,
                                              date_format=self.preferred_date_format)

        self.settings_page = SettingsPage(access_token_getter=self.get_access_token,
                                          handle_token_expired = self.handle_token_expired_or_logout,
                                          preferred_currency_display= self.preferred_currency_display,
                                          preferred_date_format=self.preferred_date_format)

        self.confirmation_dialog = MessageDialog("Logout Confirmation",
                                                 "Are you sure you want to log out?",
                                                 self.handle_token_expired_or_logout)

        self.content_stack.addWidget(self.dashboard_page)

        self.content_stack.addWidget(self.recurring_expense_page)

        self.content_stack.addWidget(self.expenses_page)

        self.content_stack.addWidget(self.incomes_page)

        self.content_stack.addWidget(self.savings_page)

        self.content_stack.addWidget(self.health_page)

        self.content_stack.addWidget(self.appointments_page)

        self.content_stack.addWidget(self.memorable_days_page)

        self.content_stack.addWidget(self.family_page)

        self.content_stack.addWidget(self.settings_page)

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

        self.center_top_bar_layout = QHBoxLayout()
        self.center_top_bar_layout.setSpacing(12)

        self.create_top_bar_month_component()

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

        self.user_profile_button.clicked.connect(self.handle_show_profile_dialog)
        top_layout.addWidget(self.top_title)
        top_layout.addStretch()
        top_layout.addLayout(self.center_top_bar_layout)
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
        if self.top_title.text().strip() == "Health":
            clear_layout(self.center_top_bar_layout)
            type_select_row = QHBoxLayout()
            type_select_row.setContentsMargins(0, 0, 0, 0)
            type_select_row.setSpacing(8)

            type_select_label = QLabel("health record type:".title())
            type_select_label.setStyleSheet("""
                        color: #334155;
                        font-size: 13px;
                    """)

            self.type_select_input = QComboBox()
            self.type_select_input.setStyleSheet(get_combo_style())
            self.type_select_input.addItem("Weight", "weight record")
            self.type_select_input.addItem("Blood Pressure", "blood pressure record")
            self.type_select_input.addItem("Blood Sugar", "blood sugar record")
            self.type_select_input.addItem("Period Record", "period record")
            self.type_select_input.setFixedHeight(36)
            self.type_select_input.setMinimumWidth(200)

            self.type_select_input.currentTextChanged.connect(self.handle_health_type_changed)



            type_select_row.addStretch()
            type_select_row.addWidget(type_select_label)
            type_select_row.addWidget(self.type_select_input)
            type_select_row.addWidget(self.create_top_bar_add_button("Add Record"
                                           ,
                                           self.handle_add_health_record_button_clicked))
            type_select_row.addStretch()
            self.center_top_bar_layout.addLayout(type_select_row)

        elif self.top_title.text().strip() == "Expenses":
                clear_layout(self.center_top_bar_layout)
                self.center_top_bar_layout.addWidget(self.create_top_bar_add_button("Add Expense"
                                                                                    ,self.handle_add_expenses_button_clicked))
        elif self.top_title.text().strip() == "Income":
            clear_layout(self.center_top_bar_layout)
            self.center_top_bar_layout.addWidget(self.create_top_bar_add_button("Add Income"
                                                                                ,
                                                                                self.handle_add_incomes_button_clicked))
        elif self.top_title.text().strip() == "Recurring Bills":
            clear_layout(self.center_top_bar_layout)
            self.center_top_bar_layout.addWidget(self.create_top_bar_add_button("Add Recurring Bill"
                                                                                ,
                                                                                self.handle_add_recurring_expense_button_clicked))
        elif self.top_title.text().strip() == "Dashboard":
            clear_layout(self.center_top_bar_layout)
            self.create_top_bar_month_component()
        elif self.top_title.text().strip() == "Appointments":
            clear_layout(self.center_top_bar_layout)
            self.center_top_bar_layout.addWidget(self.create_top_bar_add_button("Add Appointment"
                                                                                ,
                                                                                self.handle_add_appointment_button_clicked))
        else:
            clear_layout(self.center_top_bar_layout)

    def handle_login_success(self, auth_data):
        self.access_token = auth_data["access_token"]
        self.token_type = auth_data["token_type"]
        self.get_current_user_profile()
        self.setup_main_container()
        self.user_profile_button.setText(self.username)
        self.app_stack.setCurrentWidget(self.main_app_page)
        self.load_dashboard_data()


    def get_access_token(self):
        return self.access_token

    def handle_show_profile_dialog(self):

        try:

            current_user_info = get_current_user_profile(self.access_token)["data"]
            display_name = current_user_info["display_name"]
            email = current_user_info["email"]
            family_code = current_user_info["family_code"]
            self.profile_dialog = ProfileDialog(display_name,email,family_code,self.get_access_token)
            self.profile_dialog.exec()

        except requests.ConnectionError:

            connection_error_message_dialog = MessageDialog("Connection Error", "Unable to connect to the server.")

            connection_error_message_dialog.error_dialog()

            connection_error_message_dialog.exec()


        except requests.Timeout:

            timeout_error_message_dialog = MessageDialog("Connection Error", "The request timed out.")

            timeout_error_message_dialog.error_dialog()

            timeout_error_message_dialog.exec()


        except Exception as error:

            if str(error) == "Session Expired":
                self.handle_token_expired_or_logout()
                return

            api_error_message_dialog = MessageDialog("API Error", str(error))

            api_error_message_dialog.error_dialog()

            api_error_message_dialog.exec()

    def create_top_bar_month_component(self):
        self.current_month_year_label = QLabel(f"{self.current_dashboard_date.toString("MMM")} {self.current_dashboard_date.toString("yyyy")}")
        self.current_month_year_label.setStyleSheet("""
                                        color: #475569;
                                        font-size: 18px;
                                        font-weight: 600;
                                        letter-spacing: 1px;
                                    """)

        self.previous_month_button = QPushButton("      <      ")
        self.previous_month_button.setCursor(Qt.CursorShape.PointingHandCursor)
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
        self.next_month_button.setEnabled(False)
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

        self.previous_month_button.setFixedSize(40, 40)
        self.next_month_button.setFixedSize(40, 40)

        self.next_month_button.clicked.connect(self.next_month_summary_request)
        self.previous_month_button.clicked.connect(self.previous_month_summary_request)

        self.center_top_bar_layout.addWidget(self.previous_month_button)
        self.center_top_bar_layout.addWidget(self.current_month_year_label)
        self.center_top_bar_layout.addWidget(self.next_month_button)

    def previous_month_summary_request(self):

          self.current_dashboard_date = self.current_dashboard_date.addMonths(-1)

          self.current_month_year_label.setText(f"{self.current_dashboard_date.toString("MMM")} {self.current_dashboard_date.toString("yyyy")}")

          self.next_month_button.setEnabled(True)

          self.load_dashboard_data()


    def next_month_summary_request(self):

        self.current_dashboard_date = self.current_dashboard_date.addMonths(1)

        if self.current_dashboard_date.month() == QDate.currentDate().month() and self.current_dashboard_date.year() == QDate.currentDate().year():
            self.next_month_button.setEnabled(False)

        self.current_month_year_label.setText(
            f"{self.current_dashboard_date.toString("MMM")} {self.current_dashboard_date.toString("yyyy")}")

        self.load_dashboard_data()


    def load_dashboard_data(self):
        self.get_current_user_profile()
        self.dashboard_page.monthly_spending_chart.reload_currency_symbol(self.currency_symbol)
        try:
            dashboard_data = get_dashboard_data(int(self.current_dashboard_date.year()), int(self.current_dashboard_date.month()), self.get_access_token())

            self.dashboard_page.handle_value_update(self.dashboard_page.expense_card_value_label,
                                                    self.currency_symbol + f"{dashboard_data["total_expenses"]:.2f}")
            self.dashboard_page.handle_value_update(self.dashboard_page.income_card_value_label,
                                                    self.currency_symbol + f"{dashboard_data["total_incomes"]:.2f}")
            self.dashboard_page.handle_value_update(self.dashboard_page.recurring_expense_card_value_label,
                                                    self.currency_symbol + f"{dashboard_data["total_recurring_expenses"]:.2f}")
            balance = dashboard_data["total_incomes"] - dashboard_data["total_recurring_expenses"] - dashboard_data["total_expenses"]

            self.dashboard_page.handle_value_update(self.dashboard_page.balance_card_value_label,
                                                    self.currency_symbol + f"{balance:.2f}")
            self.dashboard_page.handle_value_update(self.dashboard_page.transaction_count_label_value,
                                                    str(dashboard_data["transaction_count"]))
            if dashboard_data["top_category"] == "N/A":
                self.dashboard_page.handle_value_update(self.dashboard_page.top_category_label_value, dashboard_data["top_category"])
            else:
                self.dashboard_page.handle_value_update(self.dashboard_page.top_category_label_value, dashboard_data[
                "top_category"].title() + f" ( {self.currency_symbol}{str(dashboard_data['top_category_amount'])} )")

            if dashboard_data["highest_expense_shop"] == "N/A":
                self.dashboard_page.handle_value_update(self.dashboard_page.highest_expense_label_value,
                                                        dashboard_data["highest_expense_shop"])
            else:
                highest_expense_date = str(dashboard_data["highest_expense_date"])
                match self.preferred_date_format:
                    case "DD/MM/YYYY": highest_expense_date = uk_date_format(str(dashboard_data["highest_expense_date"]))
                    case "DD MMM YYYY": highest_expense_date = long_date_format(str(dashboard_data["highest_expense_date"]))

                self.dashboard_page.handle_value_update(self.dashboard_page.highest_expense_label_value,
                                                        dashboard_data["highest_expense_shop"] + f" - {self.currency_symbol}"
                                                        + str(dashboard_data["highest_expense"]) + " - " +f" {highest_expense_date}")
            self.dashboard_page.handle_value_update(self.dashboard_page.average_daily_spending_value,
                                                    self.currency_symbol + f"{dashboard_data["average_daily_spending"]:.2f}")

            monthly_spending_chart_data = get_monthly_spending_chart_data(int(self.current_dashboard_date.year()),
                                                                          int(self.current_dashboard_date.month()),
                                                                          self.get_access_token())

            self.dashboard_page.monthly_spending_chart.update_chart(monthly_spending_chart_data)

            category_expenses_chart_data = get_monthly_category_expenses_chart_data(int(self.current_dashboard_date.year()),
                                                                                    int(self.current_dashboard_date.month()),
                                                                                    self.get_access_token())

            self.dashboard_page.category_expenses_chart.update_chart(category_expenses_chart_data)


        except requests.ConnectionError:

            connection_error_message_dialog = MessageDialog("Connection Error", "Unable to connect to the server.")

            connection_error_message_dialog.error_dialog()

            connection_error_message_dialog.exec()


        except requests.Timeout:

            timeout_error_message_dialog = MessageDialog("Connection Error", "The request timed out.")

            timeout_error_message_dialog.error_dialog()

            timeout_error_message_dialog.exec()


        except Exception as error:

            if str(error) == "Session Expired":
                self.handle_token_expired_or_logout()
                return

            api_error_message_dialog = MessageDialog("API Error", str(error))

            api_error_message_dialog.error_dialog()

            api_error_message_dialog.exec()

    def handle_health_type_changed(self):
        self.health_type = self.type_select_input.currentData()
        match self.health_type:
            case "weight record": self.health_page.health_records_tabs.setCurrentIndex(0)
            case "blood pressure record":self.health_page.health_records_tabs.setCurrentIndex(1)
            case "blood sugar record":self.health_page.health_records_tabs.setCurrentIndex(2)
            case "period record":self.health_page.health_records_tabs.setCurrentIndex(3)


    def handle_token_expired_or_logout(self):
        self.access_token = None
        self.app_stack.setCurrentWidget(self.auth_page)
        self.confirmation_dialog.reject()
        clear_layout(self.main_layout)

    def closeEvent(self, event):
        if self.access_token:
            self.confirmation_dialog.creation_confirmation_dialog(),
            self.confirmation_dialog.exec()
            event.ignore()

    def create_top_bar_add_button(self,button_text,click_handler):
        add_button = QPushButton(button_text)
        add_button.setStyleSheet("""
            QPushButton {
                background-color: #4f46e5;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 14px;
                font-size: 13px;
                font-weight: 600;
            }
            
            QPushButton:hover {
                background-color: #4338ca;
            }
            
            QPushButton:pressed {
                background-color: #3730a3;
            }
        """)

        add_button.clicked.connect(click_handler)

        return add_button


    def handle_add_expenses_button_clicked(self):
        self.get_current_user_profile()
        self.expenses_page.add_expense_dialog.set_current_date_format(self.preferred_date_format)
        self.expenses_page.add_expense_dialog.exec()

    def handle_add_incomes_button_clicked(self):
        self.incomes_page.add_income_dialog.exec()
        self.incomes_page.add_income_dialog.add_income_notify_label.setText("")

    def handle_add_recurring_expense_button_clicked(self):
        self.recurring_expense_page.add_recurring_expense_dialog.exec()
        self.recurring_expense_page.add_recurring_expense_dialog.add_recurring_expense_notify_label.setText("")

    def handle_add_appointment_button_clicked(self):
        self.appointments_page.add_appointment_dialog.exec()
        self.appointments_page.add_appointment_dialog.form_message_label.setText("")
        self.appointments_page.add_appointment_dialog.form_message_label.setStyleSheet("""
                                                                     color: #ef4444;
                                                                     font-size: 14px;
                                                                 """)

    def handle_add_health_record_button_clicked(self):
        match self.type_select_input.currentData():
            case "weight record":
                self.health_page.add_weight_record_dialog.date_format = self.preferred_date_format
                self.health_page.add_weight_record_dialog.set_current_date_format()
                self.health_page.add_weight_record_dialog.exec()
                self.health_page.add_weight_record_dialog.form_message_label.setText("")
                self.health_page.add_weight_record_dialog.form_message_label.setStyleSheet("""
                                                                     color: #ef4444;
                                                                     font-size: 14px;
                                                                 """)

            case "blood pressure record":
                self.health_page.add_blood_pressure_record_dialog.date_format = self.preferred_date_format
                self.health_page.add_blood_pressure_record_dialog.set_current_date_format()
                self.health_page.add_blood_pressure_record_dialog.exec()
                self.health_page.add_blood_pressure_record_dialog.form_message_label.setText("")
                self.health_page.add_blood_pressure_record_dialog.form_message_label.setStyleSheet("""
                                                                    color: #ef4444;
                                                                    font-size: 14px;
                                                                 """)
            case "blood sugar record":
                self.health_page.add_blood_sugar_record_dialog.date_format = self.preferred_date_format
                self.health_page.add_blood_sugar_record_dialog.set_current_date_format()
                self.health_page.add_blood_sugar_record_dialog.exec()
                self.health_page.add_blood_sugar_record_dialog.form_message_label.setText("")
                self.health_page.add_blood_sugar_record_dialog.form_message_label.setStyleSheet("""
                                                                                    color: #ef4444;
                                                                                    font-size: 14px;
                                                                                 """)
            case "period record":
                self.health_page.add_period_record_dialog.date_format = self.preferred_date_format
                self.health_page.add_period_record_dialog.change_date_format_display(self.preferred_date_format)
                self.health_page.add_period_record_dialog.exec()
                self.health_page.add_period_record_dialog.form_message_label.setText("")
                self.health_page.add_period_record_dialog.form_message_label.setStyleSheet("""
                                                                                                    color: #ef4444;
                                                                                                    font-size: 14px;
                                                                                                 """)
    def get_currency_symbol(self):

        match self.preferred_currency_display:
            case "GBP": self.currency_symbol = "£"
            case "USD": self.currency_symbol = "$"
            case "EUR": self.currency_symbol = "€"
            case "CNY": self.currency_symbol = "¥"
            case "JPY": self.currency_symbol = "¥"
            case "MYR": self.currency_symbol = "RM"

    def get_current_user_profile(self):
        try:
            user_profile = get_current_user_profile(self.access_token)["data"]

            self.username = user_profile["username"]
            self.display_name = user_profile["display_name"]
            self.preferred_date_format = user_profile["preferred_date_format"]
            self.preferred_currency_display = user_profile["preferred_currency_display"]

            self.get_currency_symbol()

        except requests.ConnectionError:

            connection_error_message_dialog = MessageDialog("Connection Error", "Unable to connect to the server.")

            connection_error_message_dialog.error_dialog()

            connection_error_message_dialog.exec()


        except requests.Timeout:

            timeout_error_message_dialog = MessageDialog("Connection Error", "The request timed out.")

            timeout_error_message_dialog.error_dialog()

            timeout_error_message_dialog.exec()


        except Exception as error:

            if str(error) == "Session Expired":
                self.handle_token_expired_or_logout()
                return

            api_error_message_dialog = MessageDialog("API Error", str(error))

            api_error_message_dialog.error_dialog()

            api_error_message_dialog.exec()



app = QApplication(sys.argv)

app.setStyleSheet("""
    QMenu {
        background-color: #ffffff;
        color: #1f2937;
        border: 1px solid #d1d5db;
        padding: 4px;
    }

    QMenu::item {
        background-color: transparent;
        color: #1f2937;
        padding: 6px 28px 6px 10px;
        border-radius: 4px;
    }

    QMenu::item:selected {
        background-color: #eef2ff;
        color: #333333;
    }

    QMenu::item:disabled {
        color: #9ca3af;
        background-color: transparent;
    }

    QMenu::separator {
        height: 1px;
        background-color: #e5e7eb;
        margin: 4px 8px;
    }
""")

font_path = (
    get_resource_directory()
    / "fonts"
    / "Inter-Regular.ttf"
)

font_id = QFontDatabase.addApplicationFont(str(font_path))
font_families = QFontDatabase.applicationFontFamilies(font_id)

font_family = font_families[0] if font_families else "Arial"

app.setFont(QFont(font_family, 10))
window = MainWindow()
window.show()
sys.exit(app.exec())