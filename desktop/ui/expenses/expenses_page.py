from PySide6.QtCore import QDate,QTimer
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QTabWidget, QPushButton, QHBoxLayout, QLabel, QTextEdit, \
    QLineEdit, QComboBox, QDateEdit, QSizePolicy, QDoubleSpinBox, QTableWidgetItem, QHeaderView, QTableWidget

from services.expense_service import get_expenses,add_expense

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

class ExpensesPage(QWidget):
    def __init__(self,access_token_getter):
        super().__init__()
        self.get_access_token = access_token_getter
        self.create_expenses_page()
        self.current_page = 1
        self.page_limit = 8
        self.total_pages = 1

    def create_expenses_page(self):

        expense_page_layout = QVBoxLayout()
        expense_page_layout.setContentsMargins(0, 0, 0, 0)
        expense_page_layout.setSpacing(16)
        self.setLayout(expense_page_layout)

        self.expense_list_card = QFrame()
        self.expense_list_card.setStyleSheet("""
            background-color: white;
            border-top-left-radius: 0px;
            border-top-right-radius: 10px;
            border-bottom-left-radius: 10px;
            border-bottom-right-radius: 10px;
        """)

        expense_list_card_layout = QVBoxLayout()
        expense_list_card_layout.setContentsMargins(20, 5, 20, 20)
        expense_list_card_layout.setSpacing(12)
        self.expense_list_card.setLayout(expense_list_card_layout)

        self.expense_tabs = QTabWidget()
        self.expense_tabs.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                top: -1px;
            }

            QTabBar::tab {
                background: #1e293b;
                color: #ffffff;
                padding: 8px 16px;
                margin-right: 4px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }

            QTabBar::tab:selected {
                background: #ffffff;
                color: #000000;
                font-weight: 600;
            }

            QTabBar::tab:!selected:hover {
                background: #334155;
                color: #ffffff;
            }
        """)

        self.create_expense_list_table()
        self.create_add_expense_card()
        self.create_expenses_filter_bar()
        self.create_expense_bottom_bar()

        expense_list_card_layout.addWidget(self.expense_filter_bar)
        expense_list_card_layout.addWidget(self.expense_table)
        expense_list_card_layout.addWidget(self.expense_bottom_bar)

        self.expense_tabs.addTab(self.expense_list_card, "Expenses")
        self.expense_tabs.addTab(self.add_expense_card, "Add Expense")

        expense_page_layout.addWidget(self.expense_tabs)

        expense_page_layout.addStretch()

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

        row_widget_one = QWidget()
        row_one_layout = QHBoxLayout()
        row_one_layout.setSpacing(12)
        row_one_layout.setContentsMargins(0, 0, 0, 0)
        row_widget_one.setLayout(row_one_layout)

        row_one_left_layout = QVBoxLayout()
        row_one_left_layout.setSpacing(4)

        amount_label_group = QWidget()
        amount_label_group_layout = QHBoxLayout()
        amount_label_group_layout.setSpacing(4)
        amount_label_group_layout.setContentsMargins(0, 0, 0, 0)
        amount_label_group.setLayout(amount_label_group_layout)

        amount_label = QLabel("Amount (£)")
        amount_label.setStyleSheet("""
            color: #334155;
            font-size: 13px;
        """)

        self.amount_error = QLabel("")
        self.amount_error.setStyleSheet("""
                    color: #ef4444;
                    font-size: 12px;
                """)

        amount_label_group_layout.addWidget(amount_label)
        amount_label_group_layout.addWidget(self.amount_error)


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


        row_one_left_layout.addWidget(amount_label_group)
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
        self.category_input.addItem("Grocery","grocery")
        self.category_input.addItem("Department Store","department store")
        self.category_input.addItem("Transport","transport")
        self.category_input.addItem("Entertainment","entertainment")
        self.category_input.addItem("Fast Food","fast food")
        self.category_input.addItem("Restaurant","restaurant")
        self.category_input.addItem("Other","other")

        self.category_input.setFixedHeight(36)
        self.category_input.setStyleSheet(self.get_combo_style())

        row_one_right_layout.addWidget(category_label)
        row_one_right_layout.addWidget(self.category_input)


        row_one_layout.addLayout(row_one_left_layout,1)
        row_one_layout.addLayout(row_one_right_layout,1)

        add_expense_card_layout.addWidget(row_widget_one)

        shop_name_label_group = QWidget()
        shop_name_label_group_layout = QHBoxLayout()
        shop_name_label_group_layout.setSpacing(4)
        shop_name_label_group_layout.setContentsMargins(0, 0, 0, 0)
        shop_name_label_group.setLayout(shop_name_label_group_layout)

        shop_name_label = QLabel("Shop Name")
        shop_name_label.setStyleSheet("""
            color: #334155;
            font-size: 13px;
        """)

        self.shop_name_error = QLabel("")
        self.shop_name_error.setStyleSheet("""
                            color: #ef4444;
                            font-size: 12px;
                        """)

        shop_name_label_group_layout.addWidget(shop_name_label)
        shop_name_label_group_layout.addWidget(self.shop_name_error)

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

        row_two_left_layout.addWidget(shop_name_label_group)
        row_two_left_layout.addWidget(self.shop_name_input)

        row_two_right_layout = QVBoxLayout()
        row_two_right_layout.setSpacing(4)

        shopping_type_label = QLabel("Shopping Type")
        shopping_type_label.setStyleSheet("""
                    color: #334155;
                    font-size: 13px;
                """)


        self.shopping_type_input = QComboBox()
        self.shopping_type_input.addItem("In-store", "in-store")
        self.shopping_type_input.addItem("Online", "online")
        self.shopping_type_input.setFixedHeight(36)
        self.shopping_type_input.setStyleSheet(self.get_combo_style())

        row_two_right_layout.addWidget(shopping_type_label)
        row_two_right_layout.addWidget(self.shopping_type_input)

        row_two_layout.addLayout(row_two_left_layout, 1)
        row_two_layout.addLayout(row_two_right_layout, 1)

        add_expense_card_layout.addWidget(row_widget_two)

        row_widget_three = QWidget()
        row_three_layout = QHBoxLayout()
        row_three_layout.setSpacing(12)
        row_three_layout.setContentsMargins(0, 0, 0, 0)
        row_widget_three.setLayout(row_three_layout)

        row_three_left_layout = QVBoxLayout()
        row_three_left_layout.setSpacing(4)

        payment_method_label = QLabel("Payment Method")
        payment_method_label.setStyleSheet("""
                            color: #334155;
                            font-size: 13px;
                        """)

        self.payment_method_input = QComboBox()
        self.payment_method_input.addItem("Card", "card")
        self.payment_method_input.addItem("Cash", "cash")
        self.payment_method_input.addItem("Voucher", "voucher")
        self.payment_method_input.setFixedHeight(36)
        self.payment_method_input.setStyleSheet(self.get_combo_style())

        row_three_left_layout.addWidget(payment_method_label)
        row_three_left_layout.addWidget(self.payment_method_input)

        row_three_right_layout = QVBoxLayout()
        row_three_right_layout.setSpacing(4)

        is_public_to_family_label = QLabel("Share With Family")
        is_public_to_family_label.setStyleSheet("""
                                    color: #334155;
                                    font-size: 13px;
                                """)

        self.is_public_to_family = QComboBox()
        self.is_public_to_family.addItems(["Yes", "No"])
        self.is_public_to_family.setFixedHeight(36)
        self.is_public_to_family.setStyleSheet(self.get_combo_style())

        row_three_right_layout.addWidget(is_public_to_family_label)
        row_three_right_layout.addWidget(self.is_public_to_family)

        row_three_layout.addLayout(row_three_left_layout, 1)
        row_three_layout.addLayout(row_three_right_layout, 1)

        add_expense_card_layout.addWidget(row_widget_three)


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
        self.date_input.setMaximumDate(QDate.currentDate())
        self.date_input.setDate(QDate.currentDate())
        self.date_input.lineEdit().setReadOnly(True)
        calendar = self.date_input.calendarWidget()
        calendar.setMinimumSize(360, 260)
        calendar.setStyleSheet("""
        QCalendarWidget {
            background-color: white;
        }

        QCalendarWidget QToolButton {
            color: #333;
            font-weight: bold;
            font-size: 14px;
        }

        QCalendarWidget QAbstractItemView {
            color: #222;
            selection-background-color: #4f46e5;
            selection-color: white;
        }
        """)

        self.date_input.setFixedHeight(36)
        self.date_input.setStyleSheet("""
                    background-color: #f8fafc;
                    border: 1px solid #e2e8f0;
                    border-radius: 6px;
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

        self.add_expense_notify_label = QLabel()
        self.add_expense_notify_label.setWordWrap(True)
        self.add_expense_notify_label.setStyleSheet("color: #22c55e;font-size: 14px;")

        add_expense_card_layout.addWidget(self.add_expense_notify_label)

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

        self.clear_button.clicked.connect(self.handle_clear_form)

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

        self.submit_button.clicked.connect(self.handle_add_expense)

        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.submit_button)

        add_expense_card_layout.addWidget(button_row)
        add_expense_card_layout.addStretch()

    def create_expense_bottom_bar(self):
        self.expense_bottom_bar = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 8, 0, 0)
        layout.setSpacing(12)
        self.expense_bottom_bar.setLayout(layout)

        self.expense_result_label = QLabel("No records loaded")
        self.expense_result_label.setStyleSheet("""
            color: #475569;
            font-size: 16px;
        """)

        self.prev_page_button = QPushButton("Previous")
        self.prev_page_button.setFixedHeight(32)
        self.prev_page_button.setStyleSheet(BOTTOM_BAR_BUTTON_STYLE)
        self.prev_page_button.setCursor(Qt.PointingHandCursor)


        self.next_page_button = QPushButton("  Next  ")
        self.next_page_button.setFixedHeight(32)
        self.next_page_button.setStyleSheet(BOTTOM_BAR_BUTTON_STYLE)
        self.next_page_button.setCursor(Qt.PointingHandCursor)

        self.prev_page_button.clicked.connect(self.handle_previous_page)
        self.next_page_button.clicked.connect(self.handle_next_page)

        layout.addWidget(self.expense_result_label)
        layout.addStretch()
        layout.addWidget(self.prev_page_button)
        layout.addWidget(self.next_page_button)

    def handle_previous_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.handle_load_expenses(
                self.payment_method_filter_input.currentData(),
                self.shopping_type_filter_input.currentData(),
                self.category_filter.currentData(),
                self.min_amount_input.text(),
                self.max_amount_input.text(),
                self.filter_start_date.date().toString("yyyy-MM-dd"),
                self.filter_end_date.date().toString("yyyy-MM-dd"),
                self.sort_by_filter_input.currentData(),
                self.sort_direction_filter_input.currentData(),
                current_page=self.current_page,
                page_limit=self.page_limit
            )

    def handle_next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.handle_load_expenses(
                self.payment_method_filter_input.currentData(),
                self.shopping_type_filter_input.currentData(),
                self.category_filter.currentData(),
                self.min_amount_input.text(),
                self.max_amount_input.text(),
                self.filter_start_date.date().toString("yyyy-MM-dd"),
                self.filter_end_date.date().toString("yyyy-MM-dd"),
                self.sort_by_filter_input.currentData(),
                self.sort_direction_filter_input.currentData(),
                current_page=self.current_page,
                page_limit=self.page_limit
            )

    def create_expenses_filter_bar(self):
        self.expense_filter_bar = QWidget()
        expense_filter_layout = QVBoxLayout()
        self.expense_filter_bar.setLayout(expense_filter_layout)

        expense_filter_row_one = QWidget()
        expense_filter_row_one.setContentsMargins(0,0,0,0)
        expense_filter_row_one_layout = QHBoxLayout()
        expense_filter_row_one.setLayout(expense_filter_row_one_layout)

        expense_filter_row_two = QWidget()
        expense_filter_row_two.setContentsMargins(0, 0, 0, 0)
        expense_filter_row_two_layout = QHBoxLayout()
        expense_filter_row_two.setLayout(expense_filter_row_two_layout)

        expense_filter_row_three = QWidget()
        expense_filter_row_three.setContentsMargins(0, 0, 0, 0)
        expense_filter_row_three_layout = QHBoxLayout()
        expense_filter_row_three.setLayout(expense_filter_row_three_layout)

        start_date_group = self.create_group_widget()

        start_date_label = QLabel("Start Date:")
        start_date_label.setStyleSheet("""
            color: #334155;
            font-size: 13px;
        """)

        self.filter_start_date = QDateEdit()
        self.filter_start_date.setFixedWidth(200)
        self.filter_start_date.setCalendarPopup(True)
        self.filter_start_date.setMaximumDate(QDate.currentDate())
        today = QDate.currentDate()
        first_day_of_current_month = QDate(today.year(), today.month(), 1)
        self.filter_start_date.setDate(first_day_of_current_month)
        self.filter_start_date.lineEdit().setReadOnly(True)
        self.filter_start_date.dateChanged.connect(lambda d: print(f"New Date: {d.toString()}"))

        self.filter_start_date.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        filter_start_date_calendar = self.filter_start_date.calendarWidget()
        filter_start_date_calendar.setMinimumSize(360, 260)
        filter_start_date_calendar.setStyleSheet("""
               QCalendarWidget {
                   background-color: white;
               }

               QCalendarWidget QToolButton {
                   color: #333;
                   font-weight: bold;
                   font-size: 14px;
               }

               QCalendarWidget QAbstractItemView {
                   color: #222;
                   selection-background-color: #4f46e5;
                   selection-color: white;
               }
               """)

        self.filter_start_date.setFixedHeight(36)
        self.filter_start_date.setStyleSheet("""
                           background-color: #f8fafc;
                           border: 1px solid #e2e8f0;
                           border-radius: 6px;
                           padding: 0 10px;
                           font-size: 14px;
                       """)

        start_date_group.layout().addWidget(start_date_label)
        start_date_group.layout().addWidget(self.filter_start_date)

        end_date_group = self.create_group_widget()

        end_date_label = QLabel("End Date:")
        end_date_label.setStyleSheet("""
                    color: #334155;
                    font-size: 13px;
                """)

        self.filter_end_date = QDateEdit()
        self.filter_end_date.setFixedWidth(200)
        self.filter_end_date.setCalendarPopup(True)
        self.filter_end_date.setMaximumDate(QDate.currentDate())
        self.filter_end_date.setDate(QDate.currentDate())
        self.filter_end_date.lineEdit().setReadOnly(True)
        self.filter_end_date.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        filter_end_date_calendar = self.filter_end_date.calendarWidget()
        filter_end_date_calendar.setMinimumSize(360, 260)
        filter_end_date_calendar.setStyleSheet("""
                       QCalendarWidget {
                           background-color: white;
                       }

                       QCalendarWidget QToolButton {
                           color: #333;
                           font-weight: bold;
                           font-size: 14px;
                       }

                       QCalendarWidget QAbstractItemView {
                           color: #222;
                           selection-background-color: #4f46e5;
                           selection-color: white;
                       }
                       """)

        self.filter_end_date.setFixedHeight(36)
        self.filter_end_date.setStyleSheet("""
                                   background-color: #f8fafc;
                                   border: 1px solid #e2e8f0;
                                   border-radius: 6px;
                                   padding: 0 10px;
                                   font-size: 14px;
                               """)

        end_date_group.layout().addWidget(end_date_label)
        end_date_group.layout().addWidget(self.filter_end_date)

        category_filter_group = self.create_group_widget()

        category_filter_label = QLabel("Category:")
        category_filter_label.setStyleSheet("""
                                    color: #334155;
                                    font-size: 13px;
                                """)

        self.category_filter = QComboBox()
        self.category_filter.setFixedWidth(200)
        self.category_filter.setMaxVisibleItems(8)
        self.category_filter.addItem("All", None)
        self.category_filter.addItem("Grocery", "grocery")
        self.category_filter.addItem("Department Store", "department store")
        self.category_filter.addItem("Transport", "transport")
        self.category_filter.addItem("Entertainment", "entertainment")
        self.category_filter.addItem("Fast Food", "fast food")
        self.category_filter.addItem("Restaurant", "restaurant")
        self.category_filter.addItem("Other", "other")

        self.category_filter.setFixedHeight(36)
        self.category_filter.setStyleSheet(self.get_combo_style())

        category_filter_group.layout().addWidget(category_filter_label)
        category_filter_group.layout().addWidget(self.category_filter)

        shopping_type_filter_group = self.create_group_widget()

        shopping_type_filter_label = QLabel("Shopping Type")
        shopping_type_filter_label.setStyleSheet("""
                            color: #334155;
                            font-size: 13px;
                        """)

        self.shopping_type_filter_input = QComboBox()
        self.shopping_type_filter_input.setFixedWidth(200)
        self.shopping_type_filter_input.addItem("All", None)
        self.shopping_type_filter_input.addItem("In-store", "in-store")
        self.shopping_type_filter_input.addItem("Online", "online")
        self.shopping_type_filter_input.setFixedHeight(36)
        self.shopping_type_filter_input.setStyleSheet(self.get_combo_style())

        shopping_type_filter_group.layout().addWidget(shopping_type_filter_label)
        shopping_type_filter_group.layout().addWidget(self.shopping_type_filter_input)

        min_amount_group = self.create_group_widget()

        min_amount_label = QLabel("Minimum Amount (£)")
        min_amount_label.setStyleSheet("""
                    color: #334155;
                    font-size: 13px;
                """)

        self.min_amount_input = QDoubleSpinBox()
        self.min_amount_input.setMinimum(0.01)
        self.min_amount_input.setMaximum(10000.00)
        self.min_amount_input.setDecimals(2)
        self.min_amount_input .setFixedWidth(170)
        self.min_amount_input.setFixedHeight(36)
        self.min_amount_input.setStyleSheet("""
                    background-color: #f8fafc;
                    border: 1px solid #e2e8f0;
                    border-radius: 6px;
                    padding: 0 10px;
                    font-size: 14px;
                """)

        min_amount_group.layout().addWidget(min_amount_label)
        min_amount_group.layout().addWidget(self.min_amount_input)

        max_amount_group = self.create_group_widget()

        max_amount_label = QLabel("Maximum Amount (£)")
        max_amount_label.setStyleSheet("""
                           color: #334155;
                           font-size: 13px;
                       """)

        self.max_amount_input = QDoubleSpinBox()
        self.max_amount_input.setMinimum(0.01)
        self.max_amount_input.setMaximum(10000.00)
        self.max_amount_input.setValue(10000)
        self.max_amount_input.setDecimals(2)
        self.max_amount_input.setFixedWidth(170)
        self.max_amount_input.setFixedHeight(36)
        self.max_amount_input.setStyleSheet("""
                           background-color: #f8fafc;
                           border: 1px solid #e2e8f0;
                           border-radius: 6px;
                           padding: 0 10px;
                           font-size: 14px;
                       """)

        max_amount_group.layout().addWidget(max_amount_label)
        max_amount_group.layout().addWidget(self.max_amount_input)

        payment_method_filter_group = self.create_group_widget()

        payment_method_filter_label = QLabel("Payment Method")
        payment_method_filter_label.setStyleSheet("""
                                    color: #334155;
                                    font-size: 13px;
                                """)

        self.payment_method_filter_input = QComboBox()
        self.payment_method_filter_input.setFixedWidth(160)
        self.payment_method_filter_input.addItem("All", None)
        self.payment_method_filter_input.addItem("Card", "card")
        self.payment_method_filter_input.addItem("Cash", "cash")
        self.payment_method_filter_input.addItem("Voucher", "voucher")
        self.payment_method_filter_input.setFixedHeight(36)
        self.payment_method_filter_input.setStyleSheet(self.get_combo_style())

        payment_method_filter_group.layout().addWidget(payment_method_filter_label)
        payment_method_filter_group.layout().addWidget(self.payment_method_filter_input)

        sort_by_filter_group = self.create_group_widget()

        sort_by_filter_label = QLabel("Sort By")
        sort_by_filter_label.setStyleSheet("""
                                            color: #334155;
                                            font-size: 13px;
                                        """)

        self.sort_by_filter_input = QComboBox()
        self.sort_by_filter_input.setFixedWidth(160)
        self.sort_by_filter_input.addItem("Date", "expense_date")
        self.sort_by_filter_input.addItem("Amount", "amount")
        self.sort_by_filter_input.setFixedHeight(36)
        self.sort_by_filter_input.setStyleSheet(self.get_combo_style())

        sort_by_filter_group.layout().addWidget(sort_by_filter_label)
        sort_by_filter_group.layout().addWidget(self.sort_by_filter_input)

        sort_direction_filter_group = self.create_group_widget()

        sort_direction_filter_label = QLabel("Sort Direction")
        sort_direction_filter_label.setStyleSheet("""
                                                   color: #334155;
                                                   font-size: 13px;
                                               """)

        self.sort_direction_filter_input = QComboBox()
        self.sort_direction_filter_input.setFixedWidth(160)
        self.sort_direction_filter_input.addItem("DESC", "desc")
        self.sort_direction_filter_input.addItem("ASC", "asc")
        self.sort_direction_filter_input.setFixedHeight(36)
        self.sort_direction_filter_input.setStyleSheet(self.get_combo_style())

        sort_direction_filter_group.layout().addWidget(sort_direction_filter_label)
        sort_direction_filter_group.layout().addWidget(self.sort_direction_filter_input)


        self.reset_filter_button = QPushButton("Reset Filter")
        self.reset_filter_button.setFixedHeight(36)
        self.reset_filter_button.setStyleSheet("""
                            QPushButton {
                                background-color: #e5e7eb;
                                color: black;
                                border-radius: 4px;
                                font-size: 14px;
                                font-weight: 600;
                                padding: 0 10px;
                            }
                            QPushButton:hover {
                                background-color: #4338ca;
                                color: white;
                            }
                        """)

        self.reset_filter_button.clicked.connect(self.handle_reset_filters)

        self.reset_filter_button.setCursor(Qt.PointingHandCursor)

        self.filter_button = QPushButton("Search Expense")
        self.filter_button.setFixedHeight(36)
        self.filter_button.setStyleSheet("""
                    QPushButton {
                        background-color: #4f46e5;
                        color: white;
                        border-radius: 4px;
                        font-size: 14px;
                        font-weight: 600;
                        padding: 0 10px;
                    }
                    QPushButton:hover {
                        background-color: #4338ca;
                    }
                """)

        self.filter_button.clicked.connect( lambda :
                                                 self.handle_load_expenses(
                                                     self.payment_method_filter_input.currentData(),
                                                     self.shopping_type_filter_input.currentData(),
                                                     self.category_filter.currentData(),
                                                     self.min_amount_input.text(),
                                                     self.max_amount_input.text(),
                                                     self.filter_start_date.date().toString("yyyy-MM-dd"),
                                                     self.filter_end_date.date().toString("yyyy-MM-dd"),
                                                     self.sort_by_filter_input.currentData(),
                                                     self.sort_direction_filter_input.currentData(),
                                                 ))
        self.filter_button.setCursor(Qt.PointingHandCursor)

        expense_filter_row_one_layout.addWidget(start_date_group)
        expense_filter_row_one_layout.addWidget(end_date_group)
        expense_filter_row_one_layout.addWidget(category_filter_group)
        expense_filter_row_one_layout.addWidget(shopping_type_filter_group)

        expense_filter_row_two_layout.addWidget(min_amount_group)
        expense_filter_row_two_layout.addWidget(max_amount_group)
        expense_filter_row_two_layout.addWidget(payment_method_filter_group)
        expense_filter_row_two_layout.addWidget(sort_by_filter_group)
        expense_filter_row_two_layout.addWidget(sort_direction_filter_group)

        expense_filter_row_three_layout.addWidget(self.reset_filter_button)
        expense_filter_row_three_layout.addWidget(self.filter_button)

        expense_filter_layout.addSpacing(10)
        expense_filter_layout.addWidget(expense_filter_row_one)
        expense_filter_layout.addWidget(expense_filter_row_two)
        expense_filter_layout.addWidget(expense_filter_row_three)

    def handle_reset_filters(self):
        self.category_filter.setCurrentIndex(0)
        self.payment_method_filter_input.setCurrentIndex(0)
        self.shopping_type_filter_input.setCurrentIndex(0)
        self.sort_by_filter_input.setCurrentIndex(0)
        self.sort_direction_filter_input.setCurrentIndex(0)

        self.min_amount_input.setValue(0.00)
        self.max_amount_input.setValue(1000.00)

        self.filter_start_date.setDate(QDate(self.filter_start_date.date().year(),
                                             self.filter_start_date.date().month(), 1))
        self.filter_end_date.setDate(QDate.currentDate())

        self.handle_load_expenses()

    def handle_load_expenses(self,payment_method=None,shopping_type=None,category=None,min_amount=None,max_amount=None,
                             start_date=None, end_date=None,sort_by=None,order=None,current_page=1,page_limit=8):
        if not start_date:
            start_date = self.filter_start_date.date().toString("yyyy-MM-dd")

        response = get_expenses(self.get_access_token(),payment_method,shopping_type,category,min_amount,max_amount,
                                start_date, end_date,sort_by,order,current_page,page_limit)

        total = response["total"]
        page = response["page"] or 1
        total_pages = response["total_pages"] or 1

        self.current_page = page
        self.total_pages = total_pages

        self.expense_table.setRowCount(len(response["data"]))

        for row,each_expense in enumerate(response["data"]):

            expense_date = QTableWidgetItem(each_expense["expense_date"])
            expense_date.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.expense_table.setItem(row, 0, QTableWidgetItem(each_expense["expense_date"]))

            shop_category = QTableWidgetItem(each_expense["category"].title())
            shop_category.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.expense_table.setItem(row, 1, shop_category)

            shop_name = QTableWidgetItem(each_expense["shop_name"])
            shop_name.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.expense_table.setItem(row, 2, shop_name)

            amount = QTableWidgetItem("£"+each_expense["amount"])
            amount.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.expense_table.setItem(row, 3, amount)

            payment = QTableWidgetItem(each_expense["payment_method"].title())
            payment.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.expense_table.setItem(row, 4, payment)

            shopping_type = QTableWidgetItem(each_expense["shopping_type"].title())
            shopping_type.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.expense_table.setItem(row, 5, shopping_type)

            self.expense_table.setItem(row, 6, QTableWidgetItem(each_expense["notes"] or ""))

        self.expense_result_label.setText(
            f"Found {total} records | Page {page} of {total_pages}"
        )

        self.prev_page_button.setEnabled(page > 1)
        self.next_page_button.setEnabled(page < total_pages)

    def create_expense_list_table(self):
        self.expense_table = QTableWidget()
        self.expense_table.setColumnCount(7)
        self.expense_table.setHorizontalHeaderLabels([
            "Date", "Category", "Shop", "Amount", "Payment", "Type", "Notes"
        ])

        self.expense_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.expense_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.expense_table.setAlternatingRowColors(True)

        self.expense_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: none;
                gridline-color: #e2e8f0;
                font-size: 13px;
            }

            QHeaderView::section {
                background-color: #e2e8f0;
                color: #0f172a;
                font-weight: 600;
                padding: 10px;
                border: none;
                border-bottom: 1px solid #cbd5e1;
            }


            }
        """)

    def handle_add_expense(self):

        if not self.validate_expense_form():
            return

        is_public_to_family = True if self.is_public_to_family.currentText() == "Yes" else False

        expense_data = {
            "amount": float(self.amount_input.text().strip()),
            "category": self.category_input.currentData(),
            "shop_name": self.shop_name_input.text().strip(),
            "shopping_type": self.shopping_type_input.currentData(),
            "payment_method": self.payment_method_input.currentData(),
            "is_public_to_family": is_public_to_family,
            "tag": self.tag_input.text().strip() or None,
            "expense_date": self.date_input.date().toString("yyyy-MM-dd"),
            "notes": self.notes_input.toPlainText().strip() or None,
        }

        try:
            add_expense(expense_data, self.get_access_token())
            self.add_expense_notify_label.setText("Successfully Added Expense")
            self.amount_input.setText("")
            self.shop_name_input.setText("")
            self.tag_input.setText("")
            self.notes_input.setPlainText("")
            self.handle_load_expenses()
            QTimer.singleShot(2000, self.clear_notify_label)
        except Exception as error:
            print("Failed to add expense:", error)

    def create_group_widget(self):

        group_widget = QWidget()
        group_widget_layout = QVBoxLayout()
        group_widget_layout.setSpacing(4)
        group_widget_layout.setContentsMargins(0, 0, 0, 0)
        group_widget.setLayout(group_widget_layout)

        return group_widget

    def handle_clear_form(self):
        self.add_expense_notify_label.setText("Form has been reset successfully")
        self.amount_input.setText("")
        self.shop_name_input.setText("")
        self.tag_input.setText("")
        self.notes_input.setPlainText("")
        QTimer.singleShot(2000, self.clear_notify_label)

    def clear_notify_label(self):
        self.add_expense_notify_label.setText("")

    def get_combo_style(self):
        return """
               QComboBox {
                   background-color: #f8fafc;
                   border: 1px solid #e2e8f0;
                   border-radius: 6px;
                   padding: 0 10px;
                   font-size: 14px;
               }

               QComboBox QAbstractItemView {
                   background-color: white;
                   border: 1px solid #e2e8f0;
                   selection-background-color: #e2e8f0;
               }
           """

    def validate_expense_form(self):
        self.amount_error.setText("")
        self.shop_name_error.setText("")
        amount_text = self.amount_input.text().strip()
        shop_name = self.shop_name_input.text().strip()

        if not amount_text:
            self.amount_error.setText("Amount Is Required")
            return False

        try:
            amount = float(amount_text)
        except ValueError:
            self.amount_error.setText("Amount Must Be A Valid Number.")
            return False

        if amount <= 0:
            self.amount_error.setText("Amount Must Be Greater Than 0.")
            return False

        if not shop_name:
            self.shop_name_error.setText("Shop Name Is Required")
            return False

        return True