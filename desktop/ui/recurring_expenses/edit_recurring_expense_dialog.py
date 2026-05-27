from datetime import timedelta, date

from PySide6.QtCore import QDate, QTimer
from PySide6.QtWidgets import QDialog, QFrame, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QLineEdit, QComboBox, \
    QDateEdit, QTextEdit, QPushButton, QMessageBox


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


def get_combo_style():
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


class EditRecurringExpenseDialog(QDialog):
    def __init__(self, handle_edit_expense, handle_delete_expense, existing_payload):
        super().__init__()
        self.display_name = None
        self.expense_id = None
        self.setWindowTitle("Update Recurring Expense")
        self.setModal(True)
        self.resize(660, 660)
        self.handle_edit_expense = handle_edit_expense
        self.handle_delete_expense = handle_delete_expense
        self.existing_payload = existing_payload
        self.create_edit_expense_card()
        self.load_existing_payload()

    def create_edit_expense_card(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(8, 8, 8, 8)
        self.setLayout(main_layout)

        self.edit_expense_card = QFrame()
        self.edit_expense_card.setStyleSheet("""
            background-color: white;
            border-radius: 10px;
        """)

        edit_expense_card_layout = QVBoxLayout()
        self.edit_expense_card.setLayout(edit_expense_card_layout)
        edit_expense_card_layout.setContentsMargins(20, 20, 20, 20)
        edit_expense_card_layout.setSpacing(12)

        row_one_layout = QHBoxLayout()
        row_one_layout.setSpacing(12)
        row_one_layout.setContentsMargins(0, 0, 0, 0)

        row_one_left_layout = QVBoxLayout()
        row_one_left_layout.setSpacing(4)

        category_label = QLabel("Category")
        category_label.setStyleSheet("""
                            color: #334155;
                            font-size: 13px;
                        """)

        self.category_input = QComboBox()
        self.category_input.addItem("Housing", "housing")
        self.category_input.addItem("Utilities", "utilities")
        self.category_input.addItem("Insurance", "insurance")
        self.category_input.addItem("Subscription", "subscription")
        self.category_input.addItem("Healthcare", "healthcare")
        self.category_input.addItem("Transport", "transport")
        self.category_input.addItem("Other", "other")

        self.category_input.setFixedHeight(36)
        self.category_input.setStyleSheet(get_combo_style())

        row_one_left_layout.addWidget(category_label)
        row_one_left_layout.addWidget(self.category_input)

        row_one_right_layout = QVBoxLayout()
        row_one_right_layout.setSpacing(4)



        subcategory_label = QLabel("Subcategory")
        subcategory_label.setStyleSheet("""
                                    color: #334155;
                                    font-size: 13px;
                                """)

        self.subcategory_input = QComboBox()
        self.subcategory_input.setFixedHeight(36)
        self.subcategory_input.setStyleSheet(get_combo_style())

        row_one_right_layout.addWidget(subcategory_label)
        row_one_right_layout.addWidget(self.subcategory_input)

        row_one_layout.addLayout(row_one_left_layout, 1)
        row_one_layout.addLayout(row_one_right_layout, 1)

        edit_expense_card_layout.addLayout(row_one_layout)

        row_two_layout = QHBoxLayout()
        row_two_layout.setSpacing(12)
        row_two_layout.setContentsMargins(0, 0, 0, 0)

        row_two_left_layout = QVBoxLayout()
        row_two_left_layout.setSpacing(4)

        amount_label_group_layout = QHBoxLayout()
        amount_label_group_layout.setSpacing(4)
        amount_label_group_layout.setContentsMargins(0, 0, 0, 0)

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

        row_two_left_layout.addLayout(amount_label_group_layout)
        row_two_left_layout.addWidget(self.amount_input)

        row_two_right_layout = QVBoxLayout()
        row_two_right_layout.setSpacing(4)

        provider_name_label_group_layout = QHBoxLayout()
        provider_name_label_group_layout.setSpacing(4)
        provider_name_label_group_layout.setContentsMargins(0, 0, 0, 0)

        provider_name_label = QLabel("Service Provider Name")
        provider_name_label.setStyleSheet("""
                            color: #334155;
                            font-size: 13px;
                        """)

        self.provider_name_error = QLabel("")
        self.provider_name_error.setStyleSheet("""
                                            color: #ef4444;
                                            font-size: 12px;
                                        """)

        provider_name_label_group_layout.addWidget(provider_name_label)
        provider_name_label_group_layout.addWidget(self.provider_name_error)

        self.provider_name_input = QLineEdit()
        self.provider_name_input.setFixedHeight(36)
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

        row_two_right_layout.addLayout(provider_name_label_group_layout)
        row_two_right_layout.addWidget(self.provider_name_input)

        row_two_layout.addLayout(row_two_left_layout, 1)
        row_two_layout.addLayout(row_two_right_layout, 1)

        edit_expense_card_layout.addLayout(row_two_layout)

        row_three_layout = QHBoxLayout()
        row_three_layout.setSpacing(12)
        row_three_layout.setContentsMargins(0, 0, 0, 0)

        row_three_left_layout = QVBoxLayout()
        row_three_left_layout.setSpacing(4)

        payment_method_label = QLabel("Payment Method")
        payment_method_label.setStyleSheet("""
                                    color: #334155;
                                    font-size: 13px;
                                """)

        self.payment_method_input = QComboBox()
        self.payment_method_input.addItem("Direct Debit", "direct debit")
        self.payment_method_input.addItem("Card", "card")
        self.payment_method_input.addItem("Bank Transfer", "bank transfer")
        self.payment_method_input.setFixedHeight(36)
        self.payment_method_input.setStyleSheet(get_combo_style())

        row_three_left_layout.addWidget(payment_method_label)
        row_three_left_layout.addWidget(self.payment_method_input)

        row_three_right_layout = QVBoxLayout()
        row_three_right_layout.setSpacing(4)

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


        row_three_right_layout.addWidget(frequency_label)
        row_three_right_layout.addWidget(self.frequency_input)

        row_three_layout.addLayout(row_three_left_layout, 1)
        row_three_layout.addLayout(row_three_right_layout, 1)

        edit_expense_card_layout.addLayout(row_three_layout)

        is_public_to_family_label = QLabel("Share With Family")
        is_public_to_family_label.setStyleSheet("""
                                                    color: #334155;
                                                    font-size: 13px;
                                                """)

        self.is_public_to_family = QComboBox()
        self.is_public_to_family.addItem("Yes", True)
        self.is_public_to_family.addItem("No", False)
        self.is_public_to_family.setFixedHeight(36)
        self.is_public_to_family.setStyleSheet(get_combo_style())

        edit_expense_card_layout.addWidget(is_public_to_family_label)
        edit_expense_card_layout.addWidget(self.is_public_to_family)

        row_four_layout = QHBoxLayout()
        row_four_layout.setSpacing(12)
        row_four_layout.setContentsMargins(0, 0, 0, 0)

        row_four_left_layout = QVBoxLayout()
        row_four_left_layout.setSpacing(4)

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

        self.start_date_input.setFixedHeight(36)
        self.start_date_input.setStyleSheet("""
                            background-color: #f8fafc;
                            border: 1px solid #e2e8f0;
                            border-radius: 6px;
                            padding: 0 10px;
                            font-size: 14px;
                        """)

        row_four_left_layout.addWidget(start_date_label)
        row_four_left_layout.addWidget(self.start_date_input)

        row_four_right_layout = QVBoxLayout()
        row_four_right_layout.setSpacing(4)

        end_date_label = QLabel("End Date")
        end_date_label.setStyleSheet("""
                           color: #334155;
                           font-size: 13px;
                       """)

        self.end_date_input = QDateEdit()

        self.end_date_input.setCalendarPopup(True)
        self.end_date_input.setMinimumDate(QDate.currentDate())
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

        self.end_date_input.setFixedHeight(36)
        self.end_date_input.setStyleSheet("""
                                   background-color: #f8fafc;
                                   border: 1px solid #e2e8f0;
                                   border-radius: 6px;
                                   padding: 0 10px;
                                   font-size: 14px;
                               """)

        row_four_right_layout.addWidget(end_date_label)
        row_four_right_layout.addWidget(self.end_date_input)

        row_four_layout.addLayout(row_four_left_layout)
        row_four_layout.addLayout(row_four_right_layout)

        edit_expense_card_layout.addLayout(row_four_layout)

        notes_label = QLabel("Notes (Optional)")
        notes_label.setStyleSheet("""
                    color: #334155;
                    font-size: 13px;
                """)

        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Add any extra details...")
        self.notes_input.setFixedHeight(100)
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

        edit_expense_card_layout.addWidget(notes_label)
        edit_expense_card_layout.addWidget(self.notes_input)

        self.update_expense_notify_label = QLabel()
        self.update_expense_notify_label.setWordWrap(True)
        self.update_expense_notify_label.setStyleSheet("color: #22c55e;font-size: 14px;")

        edit_expense_card_layout.addWidget(self.update_expense_notify_label)

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

        self.clear_button.clicked.connect(self.handle_reset_form)

        self.delete_expense_button = QPushButton("Delete Expense")
        self.delete_expense_button.setFixedHeight(40)
        self.delete_expense_button.setStyleSheet("""
                            QPushButton {
                                background-color: #ef4444;
                                color: white;
                                border-radius: 8px;
                                padding: 0 18px;
                                font-size: 14px;
                                font-weight: 600;
                            }

                            QPushButton:hover {
                                background-color: #dc2626;
                            }
                            }
                        """)

        self.delete_expense_button.clicked.connect(self.delete_expense_clicked)

        self.update_button = QPushButton("Update Expense")
        self.update_button.setFixedHeight(40)
        self.update_button.setStyleSheet("""
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

        self.update_button.clicked.connect(self.handle_update_buton_clicked)

        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.delete_expense_button)
        button_layout.addWidget(self.update_button)

        edit_expense_card_layout.addWidget(button_row)
        edit_expense_card_layout.addStretch()

        main_layout.addWidget(self.edit_expense_card)

    def load_existing_payload(self):
        self.expense_id = self.existing_payload["id"]
        self.amount_input.setText(str(self.existing_payload["amount"]))
        category_index = self.category_input.findData(self.existing_payload["category"])
        if category_index != -1:
            self.category_input.setCurrentIndex(category_index)

        self.load_subcategory(self.existing_payload["category"])
        subcategory_index = self.subcategory_input.findData(self.existing_payload["subcategory"])
        if subcategory_index != -1:
            self.subcategory_input.setCurrentIndex(subcategory_index)
        self.provider_name_input.setText(self.existing_payload["provider_name"])
        payment_method_index = self.payment_method_input.findData(self.existing_payload["payment_method"])
        if payment_method_index != -1:
            self.payment_method_input.setCurrentIndex(payment_method_index)

        payment_frequency_index = self.frequency_input.findData(self.existing_payload["frequency"])

        if payment_frequency_index != -1:
            self.frequency_input.setCurrentIndex(payment_frequency_index)

        start_date_year = self.existing_payload["start_date"]
        self.start_date_input.setDate(QDate.fromString(start_date_year, "yyyy-MM-dd"))

        if self.existing_payload["end_date"]:
            end_date_year = self.existing_payload["end_date"]
            self.end_date_input.setDate(QDate.fromString(end_date_year, "yyyy-MM-dd"))
        else:
            self.end_date_input.setSpecialValueText("No End Date")
            self.end_date_input.setDate(self.end_date_input.minimumDate())

        self.notes_input.setText(self.existing_payload["notes"])


    def handle_update_buton_clicked(self):

        if not self.validate_expense_form():
            return

        is_public_to_family = True if self.is_public_to_family.currentData() == "Yes" else False

        expenses_data = {
            "amount": float(self.amount_input.text().strip()),
            "category": self.category_input.currentData(),
            "subcategory": self.subcategory_input.currentData(),
            "provider_name": self.provider_name_input.text().strip(),
            "payment_method": self.payment_method_input.currentData(),
            "frequency": self.frequency_input.currentData(),
            "is_public_to_family": is_public_to_family,
            "start_date": self.start_date_input.date().toString("yyyy-MM-dd"),
            "end_date": self.end_date_input.date().toString(
                "yyyy-MM-dd") if self.end_date_input.date() != self.end_date_input.minimumDate() else None,
            "notes": self.notes_input.toPlainText().strip() or None,
        }

        self.handle_edit_expense(self.expense_id, expenses_data)
        self.update_expense_notify_label.setText("Successfully Updated Expense")
        QTimer.singleShot(2000, self.reject)

    def validate_expense_form(self):
        self.amount_error.setText("")
        self.provider_name_error.setText("")
        amount_text = self.amount_input.text().strip()
        provider_name = self.provider_name_input.text().strip()

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

        if not provider_name:
            self.provider_name_error.setText("Service Provider Name Is Required")
            return False

        return True

    def handle_reset_form(self):
        self.update_expense_notify_label.setText("Form has been reset successfully")
        self.amount_input.setText("")
        self.provider_name_input.setText("")
        self.notes_input.setPlainText("")
        QTimer.singleShot(2000, self.clear_notify_label)

    def clear_notify_label(self):
        self.update_expense_notify_label.setText("")

    def delete_expense_clicked(self):
        reply = QMessageBox.question(
            self,
            "Delete Expense",
            "Are you sure you want to delete this expense?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:

            self.handle_delete_expense(self.expense_id)
            self.amount_input.setText("")
            self.provider_name_input.setText("")
            self.notes_input.setPlainText("")
            self.update_expense_notify_label.setText(
                "Successfully Deleted Expense"
            )
            QTimer.singleShot(2000, self.reject)




    def load_subcategory(self, category):

        self.subcategory_input.clear()

        if category.upper() in ALLOWED_RECURRING_SUBCATEGORIES:
            for subcategory in ALLOWED_RECURRING_SUBCATEGORIES[category.upper()]:
                self.subcategory_input.addItem(subcategory.lower().title(), subcategory.lower())
