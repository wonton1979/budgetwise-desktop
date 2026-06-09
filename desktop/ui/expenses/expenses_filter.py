from PySide6.QtCore import Qt, QDate
from PySide6.QtWidgets import QWidget, QPushButton, QLabel, QComboBox, QVBoxLayout, QHBoxLayout, QDateEdit, QSizePolicy, \
    QDoubleSpinBox

from utils.combobox_style import get_combo_style


class ExpensesFilter(QWidget):
    def __init__(self,handle_on_search):
        super().__init__()
        self.handle_on_search = handle_on_search
        self.create_expenses_filter_bar()

    def create_expenses_filter_bar(self):

        expense_filter_layout = QVBoxLayout()
        self.setLayout(expense_filter_layout)

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

        self.filter_start_date.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
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
        self.filter_end_date.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
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
        self.category_filter.setStyleSheet(get_combo_style())

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
        self.shopping_type_filter_input.setStyleSheet(get_combo_style())

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
        self.payment_method_filter_input.setStyleSheet(get_combo_style())

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
        self.sort_by_filter_input.setStyleSheet(get_combo_style())

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
        self.sort_direction_filter_input.setStyleSheet(get_combo_style())

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

        self.reset_filter_button.setCursor(Qt.CursorShape.PointingHandCursor)

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
                                                 self.handle_on_search(
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
        self.filter_button.setCursor(Qt.CursorShape.PointingHandCursor)

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

        self.handle_on_search(
            self.payment_method_filter_input.currentData(),
            self.shopping_type_filter_input.currentData(),
            self.category_filter.currentData(),
            self.min_amount_input.text(),
            self.max_amount_input.text(),
            self.filter_start_date.date().toString("yyyy-MM-dd"),
            self.filter_end_date.date().toString("yyyy-MM-dd"),
            self.sort_by_filter_input.currentData(),
            self.sort_direction_filter_input.currentData(),
        )

    def create_group_widget(self):

        group_widget = QWidget()
        group_widget_layout = QVBoxLayout()
        group_widget_layout.setSpacing(4)
        group_widget_layout.setContentsMargins(0, 0, 0, 0)
        group_widget.setLayout(group_widget_layout)

        return group_widget