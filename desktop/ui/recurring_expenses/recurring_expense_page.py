from datetime import date, timedelta
from typing import cast

import requests
from PySide6.QtCore import QDate, Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFrame, QLabel,
    QPushButton, QHBoxLayout, QTreeWidget, QLineEdit, QComboBox, QDateEdit, QHeaderView, QTreeWidgetItem,
    QAbstractItemView, QTextEdit
)

from services.recurring_expense_service import add_recurring_expense, get_recurring_expense, update_recurring_expense, \
    delete_recurring_expense
from ui.components.dialogs.message_dialog import MessageDialog
from ui.recurring_expenses.edit_recurring_expense_dialog import EditRecurringExpenseDialog
from utils.combobox_style import get_combo_style

ALLOWED_RECURRING_SUBCATEGORIES = {

    "HOUSING": [
        "MORTGAGE",
        "RENT",
        "COUNCIL_TAX",
        "HOME INSURANCE",
    ],

    "UTILITIES": [
        "ELECTRICITY",
        "GAS",
        "WATER",
        "BROADBAND",
        "MOBILE_BILL",
        "TV LICENCE",
    ],

    "INSURANCE": [
        "CAR INSURANCE",
        "LIFE INSURANCE",
        "PET INSURANCE",
        "HOME EMERGENCY",
        "BREAKDOWN COVER",
        "PHONE INSURANCE",
    ],

    "SUBSCRIPTION": [
        "STREAMING",
        "TV PACKAGE",
        "GAMING SUBSCRIPTION",
        "SOFTWARE SUBSCRIPTION",
    ],

    "HEALTHCARE": [
        "MEDICAL",
        "DENTAL",
        "EYE CARE",
        "PRESCRIPTION",
    ],

    "TRANSPORT": [
        "PARKING",
        "FUEL",
        "TRANSPORT PASS",
        "CAR FINANCE",
        "ROAD TAX",
    ],

    "OTHER": [
        "OTHER",
    ],
}



class RecurringExpensePage(QWidget):
    def __init__(self,access_token_getter,handle_token_expired):
        super().__init__()
        self.get_access_token = access_token_getter
        self.handle_token_expired = handle_token_expired
        self.create_recurring_expense_page()


    def create_recurring_expense_page(self):

        recurring_expense_page_layout = QVBoxLayout()
        recurring_expense_page_layout.setContentsMargins(0, 0, 0, 0)
        recurring_expense_page_layout.setSpacing(16)
        self.setLayout(recurring_expense_page_layout)

        self.add_recurring_expense()
        self.create_tree_card()

        recurring_expense_page_layout.addWidget(self.add_recurring)
        recurring_expense_page_layout.addWidget(self.tree_card)

    def add_recurring_expense(self):
        self.add_recurring = QFrame()
        self.add_recurring.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
            }
        """)

        add_recurring_layout = QVBoxLayout()
        add_recurring_layout.setContentsMargins(18, 16, 18, 16)
        self.add_recurring.setLayout(add_recurring_layout)

        row_one_layout = QHBoxLayout()
        row_one_layout.setSpacing(12)
        row_one_layout.setContentsMargins(5, 0, 0, 8)

        row_one_left_layout = QVBoxLayout()
        row_one_left_layout.setSpacing(4)

        category_label = QLabel("Category")
        category_label.setStyleSheet("""
                                   color: #334155;
                                   font-size: 13px;
                               """)

        self.category_input = QComboBox()
        self.category_input.setFixedHeight(26)
        self.category_input.addItem("Housing", "housing")
        self.category_input.addItem("Utilities", "utilities")
        self.category_input.addItem("Insurance", "insurance")
        self.category_input.addItem("Subscription", "subscription")
        self.category_input.addItem("Healthcare", "healthcare")
        self.category_input.addItem("Transport", "transport")
        self.category_input.addItem("Other", "other")
        self.category_input.setStyleSheet(get_combo_style())

        self.category_input.currentTextChanged.connect(self.handle_category_changed)

        row_one_left_layout.addWidget(category_label)
        row_one_left_layout.addWidget(self.category_input)

        row_one_middle_layout = QVBoxLayout()
        row_one_middle_layout.setSpacing(4)

        shopping_type_label = QLabel("Subcategory")
        shopping_type_label.setStyleSheet("""
                            color: #334155;
                            font-size: 13px;
                        """)

        self.subcategory_input = QComboBox()
        self.subcategory_input.setFixedHeight(26)
        self.subcategory_input.addItem("Mortgage", "mortgage")
        self.subcategory_input.addItem("Rent", "rent")
        self.subcategory_input.addItem("Council Tax", "council tax")
        self.subcategory_input.addItem("Home Insurance", "home insurance")
        self.subcategory_input.setStyleSheet(get_combo_style())

        row_one_middle_layout.addWidget(shopping_type_label)
        row_one_middle_layout.addWidget(self.subcategory_input)

        row_one_right_layout = QVBoxLayout()
        row_one_right_layout.setSpacing(4)

        frequency_label = QLabel("Payment Frequency")
        frequency_label.setStyleSheet("""
                                    color: #334155;
                                    font-size: 13px;
                                """)

        self.frequency_input = QComboBox()
        self.frequency_input.setFixedHeight(26)
        self.frequency_input.addItem("Monthly", "monthly")
        self.frequency_input.addItem("Weekly", "weekly")
        self.frequency_input.addItem("Yearly", "yearly")
        self.frequency_input.setStyleSheet(get_combo_style())

        row_one_right_layout.addWidget(frequency_label)
        row_one_right_layout.addWidget(self.frequency_input)

        row_one_layout.addLayout(row_one_left_layout, 1)
        row_one_layout.addLayout(row_one_middle_layout, 1)
        row_one_layout.addLayout(row_one_right_layout, 1)

        row_two_layout = QHBoxLayout()
        row_two_layout.setSpacing(12)
        row_two_layout.setContentsMargins(0, 0, 0, 8)

        row_two_left_layout = QVBoxLayout()
        row_two_left_layout.setSpacing(4)

        amount_label_layout = QHBoxLayout()
        amount_label_layout.setSpacing(4)

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

        amount_label_layout.addWidget(amount_label)
        amount_label_layout.addWidget(self.amount_error)

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Enter amount")
        self.amount_input.setFixedHeight(26)
        self.amount_input.setStyleSheet("""
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

        row_two_left_layout.addLayout(amount_label_layout)
        row_two_left_layout.addWidget(self.amount_input)

        row_two_middle_layout = QVBoxLayout()
        row_two_middle_layout.setSpacing(4)

        payment_method_label = QLabel("Payment Method")
        payment_method_label.setStyleSheet("""
                                   color: #334155;
                                   font-size: 13px;
                               """)

        self.payment_method_input = QComboBox()
        self.payment_method_input.setFixedHeight(26)
        self.payment_method_input.addItem("Direct Debit", "direct debit")
        self.payment_method_input.addItem("Card", "card")
        self.payment_method_input.addItem("Bank Transfer", "bank transfer")
        self.payment_method_input.setStyleSheet(get_combo_style())

        row_two_middle_layout.addWidget(payment_method_label)
        row_two_middle_layout.addWidget(self.payment_method_input)

        row_two_right_layout = QVBoxLayout()
        row_two_right_layout.setSpacing(4)

        provider_name_label_layout = QHBoxLayout()
        provider_name_label_layout.setSpacing(4)

        provider_name_label = QLabel("Provider Name")
        provider_name_label.setStyleSheet("""
                    color: #334155;
                    font-size: 13px;
                """)

        self.provider_name_error = QLabel("")
        self.provider_name_error.setStyleSheet("""
                                    color: #ef4444;
                                    font-size: 12px;
                                """)

        provider_name_label_layout.addWidget(provider_name_label)
        provider_name_label_layout.addWidget(self.provider_name_error)


        self.provider_name_input = QLineEdit()
        self.provider_name_input.setFixedHeight(26)
        self.provider_name_input.setPlaceholderText("Service Provider")
        self.provider_name_input.setStyleSheet("""
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

        row_two_right_layout.addLayout(provider_name_label_layout)
        row_two_right_layout.addWidget(self.provider_name_input)

        row_two_layout.addLayout(row_two_left_layout, 1)
        row_two_layout.addLayout(row_two_middle_layout, 1)
        row_two_layout.addLayout(row_two_right_layout, 1)

        row_three_layout = QHBoxLayout()
        row_three_layout.setSpacing(12)
        row_three_layout.setContentsMargins(0, 0, 0, 8)

        row_three_left_layout = QVBoxLayout()
        row_three_left_layout.setSpacing(4)

        start_date_label = QLabel("Start Date")
        start_date_label.setStyleSheet("""
                   color: #334155;
                   font-size: 13px;
               """)

        self.start_date_input = QDateEdit()

        today = date.today()
        month_after = today + timedelta(days=31)

        self.start_date_input.setCalendarPopup(True)
        self.start_date_input.setMaximumDate(QDate(int(month_after.year), int(month_after.month), int(month_after.day)))
        self.start_date_input.setDate(QDate.currentDate())
        self.start_date_input.lineEdit().setReadOnly(True)
        start_date_calendar = self.start_date_input.calendarWidget()
        start_date_calendar.setMinimumSize(360, 260)
        start_date_calendar.setStyleSheet("""
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

        self.start_date_input.setFixedHeight(26)
        self.start_date_input.setStyleSheet("""
                           background-color: #f8fafc;
                           border: 1px solid #e2e8f0;
                           border-radius: 6px;
                           padding: 0 10px;
                           font-size: 14px;
                       """)

        row_three_left_layout.addWidget(start_date_label)
        row_three_left_layout.addWidget(self.start_date_input)

        row_three_middle_layout = QVBoxLayout()
        row_three_middle_layout.setSpacing(4)

        end_date_label_layout = QHBoxLayout()
        end_date_label_layout.setSpacing(4)

        end_date_label = QLabel("End Date")
        end_date_label.setStyleSheet("""
                          color: #334155;
                          font-size: 13px;
                      """)


        self.date_range_error = QLabel("")
        self.date_range_error.setStyleSheet("""
                                            color: #ef4444;
                                            font-size: 12px;
                                        """)

        end_date_label_layout.addWidget(end_date_label)
        end_date_label_layout.addWidget(self.date_range_error)

        self.end_date_input = QDateEdit()
        self.end_date_input.setMinimumDate(QDate.currentDate())
        self.end_date_input.setSpecialValueText("No End Date")
        self.end_date_input.setDate(self.end_date_input.minimumDate())
        self.end_date_input.setCalendarPopup(True)
        self.end_date_input.lineEdit().setReadOnly(True)
        end_date_calendar = self.end_date_input.calendarWidget()
        end_date_calendar.setMinimumSize(360, 260)
        end_date_calendar.setStyleSheet("""
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

        self.end_date_input.setFixedHeight(26)
        self.end_date_input.setStyleSheet("""
                                  background-color: #f8fafc;
                                  border: 1px solid #e2e8f0;
                                  border-radius: 6px;
                                  padding: 0 10px;
                                  font-size: 14px;
                              """)

        row_three_middle_layout.addLayout(end_date_label_layout)
        row_three_middle_layout.addWidget(self.end_date_input)

        row_three_right_layout = QVBoxLayout()
        row_three_right_layout.setSpacing(4)

        is_public_to_family_label = QLabel("Share With Family")
        is_public_to_family_label.setStyleSheet("""
                                            color: #334155;
                                            font-size: 13px;
                                        """)

        self.is_public_to_family = QComboBox()
        self.is_public_to_family.addItems(["Yes", "No"])
        self.is_public_to_family.setFixedHeight(26)
        self.is_public_to_family.setStyleSheet(get_combo_style())

        row_three_right_layout.addWidget(is_public_to_family_label)
        row_three_right_layout.addWidget(self.is_public_to_family)

        row_three_layout.addLayout(row_three_left_layout)
        row_three_layout.addLayout(row_three_middle_layout)
        row_three_layout.addLayout(row_three_right_layout)



        row_four_layout = QVBoxLayout()
        row_four_layout.setSpacing(4)

        notes_label = QLabel("Notes (Optional)")
        notes_label.setStyleSheet("""
                    color: #334155;
                    font-size: 13px;
                """)

        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Add any extra details...")
        self.notes_input.setFixedHeight(36)
        self.notes_input.setStyleSheet("""
                    QTextEdit {
                        background-color: #f8fafc;
                        border: 1px solid #e2e8f0;
                        border-radius: 8px;
                        padding: 8px 10px;
                        font-size: 14px;
                    }
                    QTextEdit:focus {
                            border: 1px solid #4f46e5;
                        }
                """)

        row_four_layout.addWidget(notes_label)
        row_four_layout.addWidget(self.notes_input)

        button_row_layout = QHBoxLayout()
        button_row_layout.setContentsMargins(0, 5, 0, 0)
        button_row_layout.setSpacing(12)

        self.clear_button = QPushButton("Clear")
        self.clear_button.setFixedHeight(30)
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

        self.submit_button = QPushButton("Add Recurring Expense")
        self.submit_button.setFixedHeight(30)
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

        button_row_layout.addWidget(self.clear_button)
        button_row_layout.addWidget(self.submit_button)


        add_recurring_layout.addLayout(row_one_layout)
        add_recurring_layout.addLayout(row_two_layout)
        add_recurring_layout.addLayout(row_three_layout)
        add_recurring_layout.addLayout(row_four_layout)
        add_recurring_layout.addLayout(button_row_layout)

    def create_tree_card(self):
        self.tree_card = QFrame()
        self.tree_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
            }
        """)

        self.tree_layout = QVBoxLayout()
        self.tree_layout.setContentsMargins(18, 16, 18, 16)
        self.tree_card.setLayout(self.tree_layout)

        self.recurring_tree = QTreeWidget()
        self.recurring_tree.setColumnCount(6)
        self.recurring_tree.setHeaderLabels([
            "Category / Bill",
            "Provider Name",
            "Amount",
            "Frequency",
            "Payment Method",
            "Action"
        ])

        self.recurring_tree.headerItem().setTextAlignment(
            5,
            Qt.AlignmentFlag.AlignCenter
        )

        self.recurring_tree.setRootIsDecorated(True)
        self.recurring_tree.setAlternatingRowColors(True)
        self.recurring_tree.setIndentation(24)
        self.recurring_tree.setExpandsOnDoubleClick(True)
        self.recurring_tree.setEditTriggers(QTreeWidget.EditTrigger.NoEditTriggers)

        self.recurring_tree.setSelectionMode(
            QAbstractItemView.SelectionMode.NoSelection
        )

        self.recurring_tree.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.recurring_tree.header().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.recurring_tree.header().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.recurring_tree.header().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.recurring_tree.header().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)

        self.recurring_tree.setStyleSheet("""
            QTreeWidget {
                background-color: white;
                border: none;
                font-size: 13px;
                color: #0f172a;
            }

            QTreeWidget::item {
                height: 34px;
                padding: 4px;
            }
            
            QTreeWidget::item:hover {
                background-color: #cfe0ff;
                color: #111827;
            }
            
            QHeaderView::section {
                background-color: #f8fafc;
                color: #475569;
                font-size: 13px;
                font-weight: 600;
                padding: 8px;
                border: none;
                border-bottom: 1px solid #e2e8f0;
            }
        """)

        self.recurring_tree.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.no_record_found_info_label = QLabel("")

        self.no_record_found_info_label.setStyleSheet("color: #4f46e5;font-size: 12px; font-weight: 600;")

        self.tree_layout.addWidget(self.recurring_tree)
        self.tree_layout.addWidget(self.no_record_found_info_label)

    def populate_tree(self):

        self.recurring_tree.clear()

        try:

            response =get_recurring_expense(self.get_access_token())

            for each_category in response["data"]:
                each_category_top_level = QTreeWidgetItem(
                    [
                        each_category["category"].title() + f" ( £{str(each_category["total_amount"])} )",
                        ""
                        "",
                        "",
                        ""
                    ]
                )
                for each_child_expense in each_category["expenses"]:
                    each_expense = QTreeWidgetItem([
                        each_child_expense["subcategory"].title(),
                        each_child_expense["provider_name"].title(),
                        "£"+str(each_child_expense["amount"]),
                        each_child_expense["frequency"].title(),
                        each_child_expense["payment_method"].title(),
                        ""
                    ])
                    each_expense.setTextAlignment(1, Qt.AlignmentFlag.AlignCenter)
                    each_expense.setTextAlignment(2, Qt.AlignmentFlag.AlignCenter)
                    each_expense.setTextAlignment(3, Qt.AlignmentFlag.AlignCenter)
                    each_expense.setTextAlignment(4, Qt.AlignmentFlag.AlignCenter)

                    each_category_top_level.addChild(each_expense)

                    container = QWidget()
                    container.setStyleSheet("""
                        background: transparent;
                    """)
                    button_layout = QHBoxLayout()
                    button_layout.setContentsMargins(0, 0, 0, 0)
                    button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)



                    self.recurring_tree.setItemWidget(each_expense, 5, container)
                    update_button = QPushButton("Update")
                    update_button.setFixedHeight(28)
                    update_button.setFixedWidth(100)
                    update_button.setStyleSheet("""
                                                       QPushButton {
                                                           background-color: #4f46e5;
                                                           color: white;
                                                           border-radius: 8px;
                                                           font-size: 10px;
                                                           font-weight: 600;
                                                       }
                                                       QPushButton:hover {
                                                           background-color: #4338ca;
                                                       }
                                                   """)
                    button_layout.addWidget(update_button)

                    container.setLayout(button_layout)

                    expense = each_child_expense
                    expense["category"] = each_category["category"]

                    update_button.clicked.connect(
                        lambda checked=False, payload=expense: self.open_update_recurring_expense_dialog(payload)
                    )

                    self.recurring_tree.setItemWidget(each_expense, 5, container)

                self.recurring_tree.addTopLevelItem(each_category_top_level)

        except requests.ConnectionError:

            connection_error_message_dialog = MessageDialog("Connection Error", "Unable to connect to the server.")

            connection_error_message_dialog.error_dialog()

            connection_error_message_dialog.exec()


        except requests.Timeout:

            timeout_error_message_dialog = MessageDialog("Connection Error", "The request timed out.")

            timeout_error_message_dialog.error_dialog()

            timeout_error_message_dialog.exec()


        except Exception as error:

            if str(error) == "Resource Not Found":
                self.no_record_found_info_label.setText("No recurring expenses yet. Add your first recurring expense to get started.")
                return

            if str(error) == "Session Expired":
                self.handle_token_expired()
                return

            api_error_message_dialog = MessageDialog("API Error", str(error))

            api_error_message_dialog.error_dialog()

            api_error_message_dialog.exec()




    def validate_expense_form(self):

        self.amount_error.setText("")
        self.provider_name_error.setText("")
        self.date_range_error.setText("")
        amount_text = self.amount_input.text().strip()
        provider_name = self.provider_name_input.text().strip()

        start_date_in_date:date = cast(date, self.start_date_input.date().toPython())


        if not amount_text:
            self.amount_error.setText("Amount Is Required")
            return False

        try:
            amount = float(amount_text)
        except ValueError:
            self.amount_error.setText("Amount Must Be A Valid Number")
            return False

        if amount <= 0:
            self.amount_error.setText("Amount Must Be Greater Than 0")
            return False

        if not provider_name:
            self.provider_name_error.setText("Shop Name Is Required")
            return False

        if self.end_date_input.date() != self.end_date_input.minimumDate():

            end_date_in_date:date = cast(date,self.end_date_input.date().toPython())

            days_in_range = end_date_in_date - start_date_in_date

            if self.frequency_input.currentData() == "monthly" and days_in_range.days <= 31:
                self.date_range_error.setText("Invalid Date Range")
                return False

            if self.frequency_input.currentData() == "weekly" and days_in_range.days <= 7:
                self.date_range_error.setText("Invalid Date Range")
                return False

            if self.frequency_input.currentData() == "yearly" and days_in_range.days <= 365:
                self.date_range_error.setText("Invalid Date Range")
                return False

        return True

    def handle_category_changed(self, category):

        self.subcategory_input.clear()

        if category.upper() in ALLOWED_RECURRING_SUBCATEGORIES:
            for subcategory in ALLOWED_RECURRING_SUBCATEGORIES[category.upper()]:
                self.subcategory_input.addItem(subcategory.lower().title(), subcategory.lower())


    def handle_add_expense(self):

        if not self.validate_expense_form():
            return

        is_public_to_family = True if self.is_public_to_family.currentText() == "Yes" else False

        payload = {
            "amount": float(self.amount_input.text()),
            "category": self.category_input.currentData(),
            "subcategory": self.subcategory_input.currentData(),
            "provider_name": self.provider_name_input.text().strip().title(),
            "frequency": self.frequency_input.currentData(),
            "payment_method": self.payment_method_input.currentData(),
            "start_date": self.start_date_input.date().toString("yyyy-MM-dd"),
            "end_date": self.end_date_input.date().toString("yyyy-MM-dd") if self.end_date_input.date() != self.end_date_input.minimumDate() else None,
            "is_public_to_family": is_public_to_family,
            "notes": self.notes_input.toPlainText().strip() or None,
        }


        try:
            add_recurring_expense(payload, self.get_access_token())
            info_message_box = MessageDialog("Success","Recurring Expense Added")
            info_message_box.information_dialog()
            info_message_box.exec()
            self.notes_input.setPlainText("")
            self.amount_input.setText("")
            self.provider_name_input.setText("")
            self.populate_tree()

        except requests.ConnectionError:

            connection_error_message_dialog = MessageDialog("Connection Error", "Unable to connect to the server.")

            connection_error_message_dialog.error_dialog()

            connection_error_message_dialog.exec()

        except requests.Timeout:

            timeout_error_message_dialog = MessageDialog("Connection Error", "The request timed out.")

            timeout_error_message_dialog.error_dialog()

            timeout_error_message_dialog.exec()

        except Exception as error:

            api_error_message_dialog = MessageDialog("API Error", str(error))

            api_error_message_dialog.error_dialog()

            api_error_message_dialog.exec()

            if str(error) == "Session Expired":
                self.handle_token_expired()

    def open_update_recurring_expense_dialog(self,expense):

        self.update_recurring_expense_dialog = EditRecurringExpenseDialog(
            handle_edit_expense=self.handle_update_recurring_expense,
            handle_delete_expense=self.handle_delete_recurring_expense,
            existing_payload=expense
        )

        self.update_recurring_expense_dialog.exec()

    def handle_update_recurring_expense(self,expense_id,expenses_data):

        try:
            response = update_recurring_expense(expense_id,expenses_data, self.get_access_token())
            if response:
                self.populate_tree()


        except requests.ConnectionError:

            connection_error_message_dialog = MessageDialog("Connection Error", "Unable to connect to the server.")

            connection_error_message_dialog.error_dialog()

            connection_error_message_dialog.exec()

        except requests.Timeout:

            timeout_error_message_dialog = MessageDialog("Connection Error", "The request timed out.")

            timeout_error_message_dialog.error_dialog()

            timeout_error_message_dialog.exec()

        except Exception as error:

            api_error_message_dialog = MessageDialog("API Error", str(error))

            api_error_message_dialog.error_dialog()

            api_error_message_dialog.exec()

            if str(error) == "Session Expired":
                self.handle_token_expired()

    def handle_delete_recurring_expense(self,expense_id):

        try:

            response = delete_recurring_expense(expense_id, self.get_access_token())
            if response:
                self.populate_tree()


        except requests.ConnectionError:

            connection_error_message_dialog = MessageDialog("Connection Error", "Unable to connect to the server.")

            connection_error_message_dialog.error_dialog()

            connection_error_message_dialog.exec()

        except requests.Timeout:

            timeout_error_message_dialog = MessageDialog("Connection Error", "The request timed out.")

            timeout_error_message_dialog.error_dialog()

            timeout_error_message_dialog.exec()

        except Exception as error:

            api_error_message_dialog = MessageDialog("API Error", str(error))

            api_error_message_dialog.error_dialog()

            api_error_message_dialog.exec()

            if str(error) == "Session Expired":
                self.handle_token_expired()

    def handle_clear_form(self):
        self.amount_input.setText("")
        self.provider_name_input.setText("")
        self.notes_input.setPlainText("")




