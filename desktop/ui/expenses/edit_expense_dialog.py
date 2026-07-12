from PySide6.QtCore import QDate, QTimer
from PySide6.QtWidgets import QDialog, QFrame, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QLineEdit, QComboBox, \
    QDateEdit, QTextEdit, QPushButton, QMessageBox

from utils.combobox_style import get_combo_style
from utils.date_picker_style import get_date_picker_style


class EditExpenseDialog(QDialog):
    def __init__(self,handle_edit_expense,handle_delete_expense,existing_payload,date_format):
        super().__init__()
        self.display_name = None
        self.expense_id = None
        self.date_format = date_format
        self.setWindowTitle("Update Expense")
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
        self.category_input.addItem("Grocery", "grocery")
        self.category_input.addItem("Department Store", "department store")
        self.category_input.addItem("Transport", "transport")
        self.category_input.addItem("Entertainment", "entertainment")
        self.category_input.addItem("Fast Food", "fast food")
        self.category_input.addItem("Restaurant", "restaurant")
        self.category_input.addItem("Other", "other")

        self.category_input.setFixedHeight(36)
        self.category_input.setStyleSheet(get_combo_style())

        row_one_right_layout.addWidget(category_label)
        row_one_right_layout.addWidget(self.category_input)

        row_one_layout.addLayout(row_one_left_layout, 1)
        row_one_layout.addLayout(row_one_right_layout, 1)

        edit_expense_card_layout.addWidget(row_widget_one)

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
        self.shopping_type_input.setStyleSheet(get_combo_style())

        row_two_right_layout.addWidget(shopping_type_label)
        row_two_right_layout.addWidget(self.shopping_type_input)

        row_two_layout.addLayout(row_two_left_layout, 1)
        row_two_layout.addLayout(row_two_right_layout, 1)

        edit_expense_card_layout.addWidget(row_widget_two)

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
        self.payment_method_input.setStyleSheet(get_combo_style())

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
        self.is_public_to_family.addItem("Yes",True)
        self.is_public_to_family.addItem("No",False)
        self.is_public_to_family.setFixedHeight(36)
        self.is_public_to_family.setStyleSheet(get_combo_style())

        row_three_right_layout.addWidget(is_public_to_family_label)
        row_three_right_layout.addWidget(self.is_public_to_family)

        row_three_layout.addLayout(row_three_left_layout, 1)
        row_three_layout.addLayout(row_three_right_layout, 1)

        edit_expense_card_layout.addWidget(row_widget_three)

        tag_label = QLabel("Tag (Optional)")
        tag_label.setStyleSheet("""
                    color: #334155;
                    font-size: 13px;
                """)

        self.tag_input = QLineEdit()
        self.tag_input.setPlaceholderText("e.g. Holiday, Birthday")
        self.tag_input.setFixedHeight(36)
        self.tag_input.setStyleSheet("""
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

        edit_expense_card_layout.addWidget(tag_label)
        edit_expense_card_layout.addWidget(self.tag_input)

        date_label = QLabel("Date")
        date_label.setStyleSheet("""
                    color: #334155;
                    font-size: 13px;
                """)

        self.date_input = QDateEdit()

        self.date_input.setCalendarPopup(True)
        self.date_input.setMaximumDate(QDate.currentDate())
        self.date_input.setDate(QDate.currentDate())
        self.set_current_date_format()
        self.date_input.lineEdit().setReadOnly(True)
        calendar = self.date_input.calendarWidget()
        calendar.setMinimumSize(360, 260)
        calendar.setStyleSheet(get_date_picker_style())

        self.date_input.setFixedHeight(36)
        self.date_input.setStyleSheet("""
                            background-color: #f8fafc;
                            border: 1px solid #e2e8f0;
                            border-radius: 6px;
                            padding: 0 10px;
                            font-size: 14px;
                        """)

        edit_expense_card_layout.addWidget(date_label)
        edit_expense_card_layout.addWidget(self.date_input)

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

        self.update_button.clicked.connect(self.handle_update_expense_button_clicked)

        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.delete_expense_button)
        button_layout.addWidget(self.update_button)

        edit_expense_card_layout.addWidget(button_row)
        edit_expense_card_layout.addStretch()


        main_layout.addWidget(self.edit_expense_card)

    def load_existing_payload(self):

        self.expense_id = self.existing_payload["id"]
        self.amount_input.setText(self.existing_payload["amount"])
        category_index = self.category_input.findData(self.existing_payload["category"])
        if category_index != -1:
            self.category_input.setCurrentIndex(category_index)
        self.shop_name_input.setText(self.existing_payload["shop_name"])
        shopping_type_index = self.shopping_type_input.findData(self.existing_payload["shopping_type"])
        if shopping_type_index != -1:
            self.shopping_type_input.setCurrentIndex(shopping_type_index)
        payment_method_index = self.payment_method_input.findData(self.existing_payload["payment_method"])

        if payment_method_index != -1:
            self.payment_method_input.setCurrentIndex(payment_method_index)
        is_public_to_family_index = self.is_public_to_family.findData(self.existing_payload["is_public_to_family"])
        if is_public_to_family_index != -1:
            self.is_public_to_family.setCurrentIndex(is_public_to_family_index)
        expense_date = QDate.fromString(self.existing_payload["expense_date"], "yyyy-MM-dd")
        self.date_input.setDate(expense_date)
        self.tag_input.setText(self.existing_payload["tag"])
        self.notes_input.setText(self.existing_payload["notes"])
        self.display_name = self.existing_payload["display_name"]

    def handle_update_expense_button_clicked(self):

        if not self.validate_expense_form():
            return

        is_public_to_family = True if self.is_public_to_family.currentData()== "Yes" else False

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
            "display_name": self.display_name,
        }

        self.handle_edit_expense(self.expense_id, expense_data)
        self.update_expense_notify_label.setText("Successfully Updated Expense")
        QTimer.singleShot(2000, self.reject)


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

    def handle_reset_form(self):
        self.update_expense_notify_label.setText("Form has been reset successfully")
        self.amount_input.setText("")
        self.shop_name_input.setText("")
        self.tag_input.setText("")
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
            self.shop_name_input.setText("")
            self.tag_input.setText("")
            self.notes_input.setPlainText("")
            self.update_expense_notify_label.setText(
                "Successfully Deleted Expense"
            )
            QTimer.singleShot(2000, self.reject)

    def set_current_date_format(self):

        match self.date_format:
            case "YYYY-MM-DD":
                self.date_input.setDisplayFormat("yyyy-MM-dd")
            case "DD MMM YYYY":
                self.date_input.setDisplayFormat("dd MMM yyyy")
            case "DD/MM/YYYY":
                self.date_input.setDisplayFormat("dd/MM/yyyy")

