import sys

from PySide6.QtCore import QSize, QDate
from PySide6.QtGui import QIcon,QFontDatabase,QFont
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, QPushButton,
                               QVBoxLayout, QLabel, QFrame, QStackedWidget, QLineEdit, QComboBox, QDateEdit, QTextEdit,
                               QSizePolicy)
from pathlib import Path

from backend.services.expense_service import add_expense

BASE_DIR = Path(__file__).resolve().parent

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Budget Wise Desktop")
        self.resize(1200, 780)
        self.setup_main_container()

    def setup_main_container(self):

        main_widget = QWidget()
        main_widget.setStyleSheet("background-color: #0f172a;")
        self.setCentralWidget(main_widget)

        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)

        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(16)
        self.setup_sidebar()
        self.setup_main_area()
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.main_area)


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
                self.content_stack.setCurrentWidget(self.dashboard_page)
            )
        )

        expenses_item = self.create_sidebar_button("Expenses")
        self.set_button_icon(expenses_item, "credit-card.png")
        expenses_item.clicked.connect(
            lambda: (
                self.set_active_button(expenses_item),
                self.content_stack.setCurrentWidget(self.expenses_page)
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
            lambda: self.set_active_button(recurring_item)
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


        self.dashboard_page = QWidget()
        dashboard_page_layout = QVBoxLayout()
        dashboard_page_layout.setContentsMargins(0, 0, 0, 0)
        dashboard_page_layout.setSpacing(16)
        self.dashboard_page.setLayout(dashboard_page_layout)

        self.create_content_area()
        dashboard_page_layout.addWidget(self.content_area, 0)

        self.create_chart_area()
        dashboard_page_layout.addWidget(self.chart_area, 1)

        self.create_bottom_area()
        dashboard_page_layout.addWidget(self.bottom_card, 0)

        self.content_stack.addWidget(self.dashboard_page)

        self.create_expenses_page()

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

        user_label = QLabel("User")
        user_label.setText("Yejun")
        user_label.setStyleSheet("""
                           font-size: 14px;
                           color: #374151;
                           background-color: #f3f4f6;
                           padding: 8px 14px;
                           border-radius: 8px;
                       """)

        top_layout.addWidget(self.top_title)
        top_layout.addStretch()
        top_layout.addWidget(user_label)

    def create_content_area(self):
        self.content_area = QFrame()
        self.content_area.setStyleSheet("background: transparent;")
        content_area_layout = QHBoxLayout()
        content_area_layout.setContentsMargins(0, 0, 0, 0)
        content_area_layout.setSpacing(16)
        self.content_area.setLayout(content_area_layout)
        self.content_area.setFixedHeight(120)

        self.expense_card = QFrame()
        self.income_card = QFrame()
        self.balance_card = QFrame()
        self.savings_card = QFrame()

        for each_card in [self.expense_card, self.income_card, self.balance_card,self.savings_card]:
            each_card.setStyleSheet("background-color: white; border-radius: 10px;")
            each_card.setFixedHeight(120)
            content_area_layout.addWidget(each_card)

        self.setup_metric_card(self.expense_card, "Total Expenses", "£0.00", "credit-card.png")
        self.setup_metric_card(self.income_card, "Total Income", "£0.00", "pound-sterling.png")
        self.setup_metric_card(self.balance_card, "Balance", "£0.00", "wallet.png")
        self.setup_metric_card(self.savings_card, "Savings", "£0.00", "piggy-bank.png")

    def create_chart_area(self):
        self.chart_area = QFrame()
        self.chart_area.setStyleSheet("background: transparent;")

        chart_layout = QHBoxLayout()
        chart_layout.setContentsMargins(0, 0, 0, 0)
        chart_layout.setSpacing(16)
        self.chart_area.setLayout(chart_layout)

        spending_chart = QFrame()
        category_chart = QFrame()

        for chart in [spending_chart, category_chart]:
            chart.setStyleSheet("""
                               background-color: white;
                               border-radius: 10px;
                           """)

        chart_layout.addWidget(spending_chart)
        chart_layout.addWidget(category_chart)

        spending_chart.setMinimumHeight(200)
        category_chart.setMinimumHeight(200)

        spending_chart_layout = QVBoxLayout()
        spending_chart.setLayout(spending_chart_layout)

        spending_chart_title = QLabel("Spending Trend")
        spending_chart_title.setStyleSheet("""
                           font-size: 14px;
                           font-weight: 600;
                           color: #0f172a;
                       """)
        spending_chart_layout.addWidget(spending_chart_title)
        spending_chart_layout.addStretch()

        category_chart_layout = QVBoxLayout()
        category_chart.setLayout(category_chart_layout)

        category_chart_title = QLabel("Spending Category")
        category_chart_title.setStyleSheet("""
                                   font-size: 14px;
                                   font-weight: 600;
                                   color: #0f172a;
                               """)
        category_chart_layout.addWidget(category_chart_title)
        category_chart_layout.addStretch()

    def create_bottom_area(self):
        self.bottom_card = QFrame()
        self.bottom_card.setStyleSheet("""
                           background-color: white;
                           border-radius: 12px;
                       """)
        self.bottom_card.setFixedHeight(120)

        bottom_layout = QVBoxLayout()
        self.bottom_card.setLayout(bottom_layout)
        bottom_layout.setContentsMargins(18, 16, 18, 16)

        recent_title = QLabel("Recent Expenses")
        recent_title.setStyleSheet("""
                           color: #0f172a;
                           font-size: 16px;
                           font-weight: 600;
                       """)

        placeholder = QLabel("No expenses yet")
        placeholder.setStyleSheet("""
                           color: #64748b;
                           font-size: 13px;
                       """)

        bottom_layout.addWidget(recent_title)
        bottom_layout.addWidget(placeholder)
        bottom_layout.addStretch()

    def create_expenses_page(self):
        self.expenses_page = QWidget()
        expense_page_layout = QVBoxLayout()
        expense_page_layout.setContentsMargins(0, 0, 0, 0)
        expense_page_layout.setSpacing(16)

        self.expenses_page.setLayout(expense_page_layout)

        self.create_add_expense_card()
        expense_page_layout.addWidget(self.add_expense_card,1)
        expense_page_layout.addStretch()

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

    def setup_metric_card(self, card, title, value, icon_name):
        card_layout = QVBoxLayout()
        card.setLayout(card_layout)
        card_layout.setContentsMargins(18, 14, 18, 14)

        top_row = QHBoxLayout()

        title_label = QLabel(title)
        title_label.setStyleSheet("""
            color: #64748b;
            font-size: 12px;
        """)

        icon_label = QLabel()
        icon_path = BASE_DIR / "icons" / icon_name
        icon_label.setPixmap(QIcon(str(icon_path)).pixmap(18, 18))

        top_row.addWidget(title_label)
        top_row.addStretch()
        top_row.addWidget(icon_label)

        value_label = QLabel(value)
        value_label.setStyleSheet("""
            color: #0f172a;
            font-size: 26px;
            font-weight: 700;
        """)

        card_layout.addLayout(top_row)
        card_layout.addWidget(value_label)
        card_layout.addStretch()

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

    def create_add_expense_card(self):
        self.add_expense_card = QFrame()
        self.add_expense_card.setStyleSheet("""
            background-color: white;
            border-radius: 10px;
        """)

        add_expense_card_layout = QVBoxLayout()
        self.add_expense_card.setLayout(add_expense_card_layout)
        add_expense_card_layout.setContentsMargins(20, 20, 20, 20)
        add_expense_card_layout.setSpacing(12)

        title_label = QLabel("Add Expense")
        title_label.setStyleSheet("""
            color: #0f172a;
            font-size: 18px;
            font-weight: 600;
        """)
        add_expense_card_layout.addWidget(title_label)

        row_widget_one = QWidget()
        row_one_layout = QHBoxLayout()
        row_one_layout.setSpacing(12)
        row_one_layout.setContentsMargins(0, 0, 0, 0)
        row_widget_one.setLayout(row_one_layout)

        row_one_left_layout = QVBoxLayout()
        row_one_left_layout.setSpacing(4)

        amount_label = QLabel("Amount (£)")
        amount_label.setStyleSheet("""
            color: #334155;
            font-size: 13px;
        """)

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Enter amount")
        self.amount_input.setFixedHeight(36)
        self.amount_input.setStyleSheet("""
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 0 10px;
            font-size: 14px;
        """)
        row_one_left_layout.addWidget(amount_label)
        row_one_left_layout.addWidget(self.amount_input)

        row_one_right_layout = QVBoxLayout()
        row_one_right_layout.setSpacing(4)

        category_label = QLabel("Category")
        category_label.setStyleSheet("""
            color: #334155;
            font-size: 13px;
        """)

        self.category_input = QComboBox()
        self.category_input.setMaxVisibleItems(8)
        self.category_input.addItems([
            "Grocery",
            "Department Store",
            "Transport",
            "Entertainment",
            "Fast Food",
            "Restaurant",
            "Other",
        ])
        self.category_input.setFixedHeight(36)
        self.category_input.setStyleSheet(self.get_combo_style())

        row_one_right_layout.addWidget(category_label)
        row_one_right_layout.addWidget(self.category_input)


        row_one_layout.addLayout(row_one_left_layout,1)
        row_one_layout.addLayout(row_one_right_layout,1)

        add_expense_card_layout.addWidget(row_widget_one)

        shop_name_label = QLabel("Shop Name")
        shop_name_label.setStyleSheet("""
            color: #334155;
            font-size: 13px;
        """)

        row_widget_two = QWidget()
        row_two_layout = QHBoxLayout()
        row_two_layout.setSpacing(12)
        row_two_layout.setContentsMargins(0, 0, 0, 0)
        row_widget_two.setLayout(row_two_layout)

        row_two_left_layout = QVBoxLayout()
        row_two_left_layout.setSpacing(4)

        self.shop_name_input = QLineEdit()
        self.shop_name_input.setPlaceholderText("e.g. Tesco, M&S, Home Bargains")
        self.shop_name_input.setFixedHeight(36)
        self.shop_name_input.setStyleSheet("""
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 0 10px;
            font-size: 14px;
        """)

        row_two_left_layout.addWidget(shop_name_label)
        row_two_left_layout.addWidget(self.shop_name_input)

        row_two_right_layout = QVBoxLayout()
        row_two_right_layout.setSpacing(4)

        shopping_type_label = QLabel("Shopping Type")
        shopping_type_label.setStyleSheet("""
                    color: #334155;
                    font-size: 13px;
                """)

        self.shopping_type_input = QComboBox()
        self.shopping_type_input.addItems(["In-store", "Online"])
        self.shopping_type_input.setFixedHeight(36)
        self.shopping_type_input.setStyleSheet(self.get_combo_style())

        row_two_right_layout.addWidget(shopping_type_label)
        row_two_right_layout.addWidget(self.shopping_type_input)

        row_two_layout.addLayout(row_two_left_layout, 1)
        row_two_layout.addLayout(row_two_right_layout, 1)

        add_expense_card_layout.addWidget(row_widget_two)

        payment_method_label = QLabel("Payment Method")
        payment_method_label.setStyleSheet("""
                            color: #334155;
                            font-size: 13px;
                        """)

        self.payment_method_input = QComboBox()
        self.payment_method_input.addItems(["Card", "Cash", "Voucher", "Mixed"])
        self.payment_method_input.setFixedHeight(36)
        self.payment_method_input.setStyleSheet(self.get_combo_style())
        add_expense_card_layout.addWidget(payment_method_label)
        add_expense_card_layout.addWidget(self.payment_method_input)

        tag_label = QLabel("Tag (Optional)")
        tag_label.setStyleSheet("""
            color: #334155;
            font-size: 13px;
        """)

        self.tag_input = QLineEdit()
        self.tag_input.setPlaceholderText("e.g. Holiday, Birthday")
        self.tag_input.setFixedHeight(36)
        self.tag_input.setStyleSheet("""
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 0 10px;
            font-size: 14px;
        """)

        add_expense_card_layout.addWidget(tag_label)
        add_expense_card_layout.addWidget(self.tag_input)

        date_label = QLabel("Date")
        date_label.setStyleSheet("""
            color: #334155;
            font-size: 13px;
        """)

        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setFixedHeight(36)
        self.date_input.setStyleSheet("""
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 0 10px;
            font-size: 14px;
        """)

        add_expense_card_layout.addWidget(date_label)
        add_expense_card_layout.addWidget(self.date_input)

        notes_label = QLabel("Notes (Optional)")
        notes_label.setStyleSheet("""
            color: #334155;
            font-size: 13px;
        """)

        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Add any extra details...")
        self.notes_input.setFixedHeight(100)
        self.notes_input.setStyleSheet("""
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 8px 10px;
            font-size: 14px;
        """)

        add_expense_card_layout.addWidget(notes_label)
        add_expense_card_layout.addWidget(self.notes_input)

        button_row = QWidget()
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 20, 0, 0)
        button_layout.setSpacing(12)
        button_row.setLayout(button_layout)

        self.clear_button = QPushButton("Clear")
        self.clear_button.setFixedHeight(40)
        self.clear_button.setStyleSheet("""
            QPushButton {
                background-color: #e5e7eb;
                color: #374151;
                border-radius: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #d1d5db;
            }
        """)

        self.submit_button = QPushButton("Add Expense")
        self.submit_button.setFixedHeight(40)
        self.submit_button.setStyleSheet("""
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

        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.submit_button)

        add_expense_card_layout.addWidget(button_row)
        add_expense_card_layout.addStretch()

    def get_combo_style(self):
        return """
            QComboBox {
                background-color: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 0 10px;
                font-size: 14px;
            }

            QComboBox QAbstractItemView {
                background-color: white;
                border: 1px solid #e2e8f0;
                selection-background-color: #e2e8f0;
            }
        """

app = QApplication(sys.argv)
font_id = QFontDatabase.addApplicationFont("fonts/Inter-Regular.ttf")
font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
app.setFont(QFont(font_family, 10))
window = MainWindow()
window.show()
sys.exit(app.exec())