from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QDialog, QFrame, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QLineEdit, QComboBox, \
    QTextEdit, QPushButton, QMessageBox

from utils.combobox_style import get_combo_style


class EditIncomeDialog(QDialog):
    def __init__(self, handle_edit_income, handle_delete_income, existing_income):
        super().__init__()
        self.income_id = None
        self.setWindowTitle("Update Income")
        self.setModal(True)
        self.resize(660, 430)
        self.handle_edit_income = handle_edit_income
        self.handle_delete_income = handle_delete_income
        self.existing_payload = existing_income
        self.create_edit_income_card()
        self.load_existing_payload()

    def create_edit_income_card(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(8, 8, 8, 8)
        self.setLayout(main_layout)

        self.edit_income_card = QFrame()
        self.edit_income_card.setStyleSheet("""
            background-color: white;
            border-radius: 10px;
        """)

        edit_income_card_layout = QVBoxLayout()
        self.edit_income_card.setLayout(edit_income_card_layout)
        edit_income_card_layout.setContentsMargins(20, 20, 20, 20)
        edit_income_card_layout.setSpacing(12)

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

        self.income_category_input = QComboBox()
        self.income_category_input.setStyleSheet(get_combo_style())
        self.income_category_input.addItem("Salary", "salary")
        self.income_category_input.addItem("Bonus", "bonus")
        self.income_category_input.addItem("Freelance", "freelance")
        self.income_category_input.addItem("Benefits", "benefits")
        self.income_category_input.addItem("Rental Income", "rental income")
        self.income_category_input.addItem("Investment", "investment")
        self.income_category_input.addItem("Pension", "pension")
        self.income_category_input.addItem("Other", "other")
        self.income_category_input.setFixedHeight(36)


        row_one_left_layout.addWidget(category_label)
        row_one_left_layout.addWidget(self.income_category_input)

        row_one_right_layout = QVBoxLayout()
        row_one_right_layout.setSpacing(4)

        income_frequency_label = QLabel("Income Frequency")
        income_frequency_label.setStyleSheet("""
                                                   color: #334155;
                                                   font-size: 13px;
                                               """)

        self.income_frequency_input = QComboBox()
        self.income_frequency_input.setStyleSheet(get_combo_style())
        self.income_frequency_input.addItem("Monthly", "monthly")
        self.income_frequency_input.addItem("Weekly", "weekly")
        self.income_frequency_input.addItem("Yearly", "yearly")
        self.income_frequency_input.addItem("Quarterly", "quarterly")
        self.income_frequency_input.setFixedHeight(36)

        row_one_right_layout.addWidget(income_frequency_label)
        row_one_right_layout.addWidget(self.income_frequency_input)

        row_one_layout.addLayout(row_one_left_layout, 1)
        row_one_layout.addLayout(row_one_right_layout, 1)

        edit_income_card_layout.addLayout(row_one_layout)

        row_two_layout = QHBoxLayout()
        row_two_layout.setSpacing(12)
        row_two_layout.setContentsMargins(0, 0, 0, 0)

        row_two_left_layout = QVBoxLayout()
        row_two_left_layout.setSpacing(4)

        amount_label_group_layout = QHBoxLayout()
        amount_label_group_layout.setSpacing(4)
        amount_label_group_layout.setContentsMargins(0, 0, 0, 0)

        amount_label = QLabel("Income Amount (£)")
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

        source_name_label_group_layout = QHBoxLayout()
        source_name_label_group_layout.setSpacing(4)
        source_name_label_group_layout.setContentsMargins(0, 0, 0, 0)

        source_name_label = QLabel("Source Name")
        source_name_label.setStyleSheet("""
                            color: #334155;
                            font-size: 13px;
                        """)

        self.source_name_error = QLabel("")
        self.source_name_error.setStyleSheet("""
                                            color: #ef4444;
                                            font-size: 12px;
                                        """)

        source_name_label_group_layout.addWidget(source_name_label)
        source_name_label_group_layout.addWidget(self.source_name_error)

        self.source_name_input = QLineEdit()
        self.source_name_input.setFixedHeight(36)
        self.source_name_input.setStyleSheet("""
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

        row_two_right_layout.addLayout(source_name_label_group_layout)
        row_two_right_layout.addWidget(self.source_name_input)

        row_two_layout.addLayout(row_two_left_layout, 1)
        row_two_layout.addLayout(row_two_right_layout, 1)

        edit_income_card_layout.addLayout(row_two_layout)

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

        edit_income_card_layout.addWidget(notes_label)
        edit_income_card_layout.addWidget(self.notes_input)

        self.update_income_notify_label = QLabel()
        self.update_income_notify_label.setWordWrap(True)
        self.update_income_notify_label.setStyleSheet("color: #22c55e;font-size: 14px;")

        edit_income_card_layout.addWidget(self.update_income_notify_label)

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

        self.delete_expense_button = QPushButton("Delete Income")
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

        self.delete_expense_button.clicked.connect(self.delete_income_clicked)

        self.update_button = QPushButton("Update Income")
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

        edit_income_card_layout.addWidget(button_row)
        edit_income_card_layout.addStretch()

        main_layout.addWidget(self.edit_income_card)

    def load_existing_payload(self):
        self.income_id = self.existing_payload["id"]
        self.amount_input.setText(str(self.existing_payload["amount"]))
        self.source_name_input.setText(self.existing_payload["source_name"])
        category_index = self.income_category_input.findData(self.existing_payload["category"])
        if category_index != -1:
            self.income_category_input.setCurrentIndex(category_index)

        income_frequency_index = self.income_frequency_input.findData(self.existing_payload["frequency"])

        if income_frequency_index != -1:
            self.income_frequency_input.setCurrentIndex(income_frequency_index)

        self.notes_input.setText(self.existing_payload["notes"])


    def handle_update_buton_clicked(self):

        if not self.validate_income_form():
            return

        income_data = {
            "amount": float(self.amount_input.text().strip()),
            "category": self.income_category_input.currentData(),
            "source_name": self.source_name_input.text().strip(),
            "frequency": self.income_frequency_input.currentData(),
            "notes": self.notes_input.toPlainText().strip() or None,
        }

        self.handle_edit_income(self.income_id, income_data)
        self.update_income_notify_label.setText("Successfully Updated Expense")
        QTimer.singleShot(2000, self.reject)

    def validate_income_form(self):
        self.amount_error.setText("")
        self.source_name_error.setText("")
        amount_text = self.amount_input.text().strip()
        source_name = self.source_name_input.text().strip()

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

        if not source_name:
            self.source_name_error.setText("Source Name Is Required")
            return False

        return True

    def handle_reset_form(self):
        self.update_income_notify_label.setText("Form has been reset successfully")
        self.amount_input.setText("")
        self.source_name_input.setText("")
        self.notes_input.setPlainText("")
        QTimer.singleShot(2000, self.clear_notify_label)

    def clear_notify_label(self):
        self.update_income_notify_label.setText("")

    def delete_income_clicked(self):
        reply = QMessageBox.question(
            self,
            "Delete Income",
            "Are you sure you want to delete this income?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:

            self.handle_delete_income(self.income_id)
            self.amount_input.setText("")
            self.source_name_input.setText("")
            self.notes_input.setPlainText("")
            self.update_income_notify_label.setText(
                "Successfully Deleted Income"
            )
            QTimer.singleShot(2000, self.reject)

