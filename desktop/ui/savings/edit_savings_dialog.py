from PySide6.QtCore import QTimer, QDate
from PySide6.QtWidgets import QDialog, QFrame, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QLineEdit, \
    QTextEdit, QPushButton, QMessageBox, QDateEdit

from utils.uk_date_format import uk_date_format


class EditSavingsDialog(QDialog):
    def __init__(self, handle_edit_savings, handle_delete_savings, existing_savings_data):
        super().__init__()
        self.savings_id = None
        self.setWindowTitle("Update Savings")
        self.setModal(True)
        self.resize(660, 430)
        self.handle_edit_savings = handle_edit_savings
        self.handle_delete_savings = handle_delete_savings
        self.existing_payload = existing_savings_data
        self.create_edit_savings_card()
        self.load_existing_payload()

    def create_edit_savings_card(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(8, 8, 8, 8)
        self.setLayout(main_layout)

        self.edit_savings_card = QFrame()
        self.edit_savings_card.setStyleSheet("""
            background-color: white;
            border-radius: 10px;
        """)

        edit_savings_card_layout = QVBoxLayout()
        self.edit_savings_card.setLayout(edit_savings_card_layout)
        edit_savings_card_layout.setContentsMargins(20, 20, 20, 20)
        edit_savings_card_layout.setSpacing(12)

        row_one_layout = QHBoxLayout()
        row_one_layout.setSpacing(12)
        row_one_layout.setContentsMargins(0, 0, 0, 0)

        row_one_left_layout = QVBoxLayout()
        row_one_left_layout.setSpacing(4)

        savings_name_label_group_layout = QHBoxLayout()
        savings_name_label_group_layout.setSpacing(4)
        savings_name_label_group_layout.setContentsMargins(0, 0, 0, 0)

        savings_name_label = QLabel("Savings Name")
        savings_name_label.setStyleSheet("""
                                   color: #334155;
                                   font-size: 13px;
                               """)

        self.savings_name_error = QLabel("")
        self.savings_name_error.setStyleSheet("""
                                                   color: #ef4444;
                                                   font-size: 12px;
                                               """)

        savings_name_label_group_layout.addWidget(savings_name_label)
        savings_name_label_group_layout.addWidget(self.savings_name_error)

        self.savings_name_input = QLineEdit()
        self.savings_name_input.setFixedHeight(36)
        self.savings_name_input.setStyleSheet("""
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


        row_one_left_layout.addLayout(savings_name_label_group_layout)
        row_one_left_layout.addWidget(self.savings_name_input)

        row_one_right_layout = QVBoxLayout()
        row_one_right_layout.setSpacing(4)

        goal_amount_label_group_layout = QHBoxLayout()
        goal_amount_label_group_layout.setSpacing(4)
        goal_amount_label_group_layout.setContentsMargins(0, 0, 0, 0)

        goal_amount_label = QLabel("Goal Amount (£)")
        goal_amount_label.setStyleSheet("""
                                   color: #334155;
                                   font-size: 13px;
                               """)

        self.goal_amount_error = QLabel("")
        self.goal_amount_error.setStyleSheet("""
                                           color: #ef4444;
                                           font-size: 12px;
                                       """)

        goal_amount_label_group_layout.addWidget(goal_amount_label)
        goal_amount_label_group_layout.addWidget(self.goal_amount_error)

        self.goal_amount_input = QLineEdit()
        self.goal_amount_input.setPlaceholderText("Enter amount")
        self.goal_amount_input.setFixedHeight(36)
        self.goal_amount_input.setStyleSheet("""
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

        row_one_right_layout.addLayout(goal_amount_label_group_layout)
        row_one_right_layout.addWidget(self.goal_amount_input)

        row_one_layout.addLayout(row_one_left_layout, 1)
        row_one_layout.addLayout(row_one_right_layout, 1)

        edit_savings_card_layout.addLayout(row_one_layout)

        row_two_layout = QHBoxLayout()
        row_two_layout.setSpacing(12)
        row_two_layout.setContentsMargins(0, 0, 0, 0)

        row_two_left_layout = QVBoxLayout()
        row_two_left_layout.setSpacing(4)

        current_amount_label_group_layout = QHBoxLayout()
        current_amount_label_group_layout.setSpacing(4)
        current_amount_label_group_layout.setContentsMargins(0, 0, 0, 0)

        current_amount_label = QLabel("Current Amount (£)")
        current_amount_label.setStyleSheet("""
                            color: #334155;
                            font-size: 13px;
                        """)

        self.current_amount_error = QLabel("")
        self.current_amount_error.setStyleSheet("""
                                    color: #ef4444;
                                    font-size: 12px;
                                """)

        current_amount_label_group_layout.addWidget(current_amount_label)
        current_amount_label_group_layout.addWidget(self.current_amount_error)

        self.current_amount_input = QLineEdit()
        self.current_amount_input.setPlaceholderText("Enter amount")
        self.current_amount_input.setFixedHeight(36)
        self.current_amount_input.setStyleSheet("""
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

        row_two_left_layout.addLayout(current_amount_label_group_layout)
        row_two_left_layout.addWidget(self.current_amount_input)

        row_two_right_layout = QVBoxLayout()
        row_two_right_layout.setSpacing(4)

        target_date_label = QLabel("End Date")
        target_date_label.setStyleSheet("""
                                  color: #334155;
                                  font-size: 13px;
                              """)

        self.target_date_input = QDateEdit()

        self.target_date_input.setCalendarPopup(True)
        self.target_date_input.lineEdit().setReadOnly(True)
        target_date_calendar = self.target_date_input.calendarWidget()
        target_date_calendar.setMinimumSize(360, 260)
        target_date_calendar.setStyleSheet("""
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

        self.target_date_input.setFixedHeight(36)
        self.target_date_input.setStyleSheet("""
                                          background-color: #f8fafc;
                                          border: 1px solid #e2e8f0;
                                          border-radius: 6px;
                                          padding: 0 10px;
                                          font-size: 14px;
                                      """)

        row_two_right_layout.addWidget(target_date_label)
        row_two_right_layout.addWidget(self.target_date_input)

        row_two_layout.addLayout(row_two_left_layout, 1)
        row_two_layout.addLayout(row_two_right_layout, 1)

        edit_savings_card_layout.addLayout(row_two_layout)

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

        edit_savings_card_layout.addWidget(notes_label)
        edit_savings_card_layout.addWidget(self.notes_input)

        self.update_income_notify_label = QLabel()
        self.update_income_notify_label.setWordWrap(True)
        self.update_income_notify_label.setStyleSheet("color: #22c55e;font-size: 14px;")

        edit_savings_card_layout.addWidget(self.update_income_notify_label)

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

        self.delete_expense_button = QPushButton("Delete Savings")
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

        self.delete_expense_button.clicked.connect(self.delete_savings_clicked)

        self.update_button = QPushButton("Update Savings")
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

        self.update_button.clicked.connect(self.handle_update_savings_clicked)

        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.delete_expense_button)
        button_layout.addWidget(self.update_button)

        edit_savings_card_layout.addWidget(button_row)
        edit_savings_card_layout.addStretch()

        main_layout.addWidget(self.edit_savings_card)

    def load_existing_payload(self):
        if self.existing_payload["target_date"]:
            self.target_date_input.setDate(QDate.fromString(uk_date_format(self.existing_payload["target_date"]), "dd/MM/yyyy"))
        else:
            self.target_date_input.setMinimumDate(QDate.currentDate())
            self.target_date_input.setSpecialValueText("No Target Date")
            self.target_date_input.setDate(self.target_date_input.minimumDate())
        self.savings_id = self.existing_payload["id"]
        self.goal_amount_input.setText(str(self.existing_payload["goal_amount"]))
        self.current_amount_input.setText(str(self.existing_payload["current_amount"]))
        self.savings_name_input.setText(self.existing_payload["purpose_name"])

        self.notes_input.setText(self.existing_payload["notes"])


    def handle_update_savings_clicked(self):

        if not self.validate_update_savings_form():
            return

        updated_savings_data = {
            "goal_amount": float(self.goal_amount_input.text().strip()),
            "current_amount": float(self.current_amount_input.text().strip()),
            "purpose_name": self.savings_name_input.text().strip(),
            "target_date": self.target_date_input.date().toString(
                "yyyy-MM-dd") if self.target_date_input.date() != self.target_date_input.minimumDate() else None,
            "notes": self.notes_input.toPlainText().strip() or None,
        }

        self.handle_edit_savings(self.savings_id, updated_savings_data)
        self.update_income_notify_label.setText("Successfully Updated Savings")
        QTimer.singleShot(2000, self.reject)

    def validate_update_savings_form(self):
        self.goal_amount_error.setText("")
        self.savings_name_error.setText("")
        self.current_amount_error.setText("")

        goal_amount_text = self.goal_amount_input.text().strip()
        current_amount_text = self.current_amount_input.text().strip()
        savings_name = self.savings_name_input.text().strip()

        if not goal_amount_text:
            self.goal_amount_error.setText("Amount Is Required")
            return False

        if not current_amount_text:
            self.current_amount_error.setText("Amount Is Required")
            return False

        try:
            goal_amount = float(goal_amount_text)
        except ValueError:
            self.goal_amount_error.setText("Amount Must Be A Valid Number")
            return False

        try:
            current_amount = float(current_amount_text)
        except ValueError:
            self.current_amount_error.setText("Amount Must Be A Valid Number")
            return False

        if goal_amount <= 0:
            self.goal_amount_error.setText("Amount Must Be Greater Than Zero")
            return False

        if current_amount < 0:
            self.current_amount_error.setText("Amount Can't Be Negative")
            return False

        if not savings_name:
            self.savings_name_error.setText("Savings Name Is Required")
            return False

        return True

    def handle_reset_form(self):
        self.update_income_notify_label.setText("Form has been reset successfully")
        self.goal_amount_input.setText("")
        self.savings_name_input.setText("")
        self.notes_input.setPlainText("")
        QTimer.singleShot(2000, self.clear_notify_label)

    def clear_notify_label(self):
        self.update_income_notify_label.setText("")

    def delete_savings_clicked(self):
        reply = QMessageBox.question(
            self,
            "Delete Savings",
            "Are you sure you want to delete this savings?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:

            self.handle_delete_savings(self.savings_id)
            self.goal_amount_input.setText("")
            self.savings_name_input.setText("")
            self.notes_input.setPlainText("")
            self.current_amount_input.setText("")
            self.update_income_notify_label.setText(
                "Successfully Deleted Savings"
            )
            QTimer.singleShot(2000, self.reject)

