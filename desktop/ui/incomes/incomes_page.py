import requests
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QHBoxLayout, QLabel, QLineEdit, QComboBox, QTextEdit, \
    QPushButton, QDateEdit

from services.income_service import add_income, get_income_by_user_id, update_income_by_income_id, \
    delete_income_by_income_id
from ui.components.dialogs.message_dialog import MessageDialog
from ui.incomes.edit_income_dialog import EditIncomeDialog
from utils.clear_layout import clear_layout
from utils.combobox_style import get_combo_style


class IncomesPage(QWidget):
    def __init__(self,access_token_getter,handle_token_expired):
        super().__init__()
        self.details_container = None
        self.get_access_token = access_token_getter
        self.handle_token_expired = handle_token_expired
        self.categorized_incomes_cards = []
        self.create_incomes_expense_page()
        self.loading_finished = False



    def create_incomes_expense_page(self):
        self.incomes_page_layout = QVBoxLayout()
        self.incomes_page_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.incomes_page_layout)

        self.add_income_frame()
        self.income_details_widget()

        self.incomes_page_layout.addWidget(self.add_income_card)
        self.incomes_page_layout.addWidget(self.details_container)

    def add_income_frame(self):
        self.add_income_card = QFrame()
        self.add_income_card.setStyleSheet("""
                    QFrame {
                        background-color: white;
                        border-radius: 10px;
                    }
                """)
        self.add_income_card.setFixedHeight(230)

        add_income_layout = QVBoxLayout()
        add_income_layout.setContentsMargins(10, 10, 10, 10)
        add_income_layout.setSpacing(4)
        self.add_income_card.setLayout(add_income_layout)

        row_one_layout = QHBoxLayout()
        row_one_layout.setContentsMargins(0, 10, 0, 0)
        row_one_layout.setSpacing(8)

        row_one_left_layout = QVBoxLayout()
        row_one_left_layout.setSpacing(4)

        income_category_label = QLabel("Income Category")
        income_category_label.setStyleSheet("""
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

        row_one_left_layout.addWidget(income_category_label)
        row_one_left_layout.addWidget(self.income_category_input )

        row_one_middle_layout = QVBoxLayout()
        row_one_middle_layout.setSpacing(4)

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
                                    font-size: 13px;
                                """)

        amount_label_layout.addWidget(amount_label)
        amount_label_layout.addWidget(self.amount_error)

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

        row_one_middle_layout.addLayout(amount_label_layout)
        row_one_middle_layout.addWidget(self.amount_input)


        row_one_right_layout = QVBoxLayout()
        row_one_right_layout.setSpacing(4)

        source_name_label_layout = QHBoxLayout()
        source_name_label_layout.setSpacing(4)

        source_name_label = QLabel("Source Name")
        source_name_label.setStyleSheet("""
                                                  color: #334155;
                                                  font-size: 13px;
                                              """)

        self.source_name_error = QLabel("")
        self.source_name_error.setStyleSheet("""
                                                           color: #ef4444;
                                                           font-size: 13px;
                                                       """)

        source_name_label_layout.addWidget(source_name_label)
        source_name_label_layout.addWidget(self.source_name_error)

        self.source_name_input = QLineEdit()
        self.source_name_input.setPlaceholderText("Enter income source name")
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


        row_one_right_layout.addLayout(source_name_label_layout)
        row_one_right_layout.addWidget(self.source_name_input)


        row_one_layout.addLayout(row_one_left_layout,1)
        row_one_layout.addLayout(row_one_middle_layout,1)
        row_one_layout.addLayout(row_one_right_layout,1)

        row_two_layout = QHBoxLayout()
        row_two_layout.setContentsMargins(0, 10, 0, 0)
        row_two_layout.setSpacing(8)

        row_two_left_layout = QVBoxLayout()
        row_two_left_layout.setSpacing(4)

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
        self.income_frequency_input.addItem("One Off", "one off")
        self.income_frequency_input.setFixedHeight(36)

        self.income_frequency_input.currentTextChanged.connect(self.handle_is_recurring_value_changed)

        row_two_left_layout.addWidget(income_frequency_label)
        row_two_left_layout.addWidget(self.income_frequency_input)

        row_two_middle_layout = QVBoxLayout()
        row_two_middle_layout.setSpacing(4)

        received_date_label = QLabel("Date")
        received_date_label.setStyleSheet("""
                    color: #334155;
                    font-size: 13px;
                """)

        self.received_date_input = QDateEdit()

        self.received_date_input.setCalendarPopup(True)
        self.received_date_input.setMaximumDate(QDate.currentDate())
        self.received_date_input.setDate(QDate.currentDate())
        self.received_date_input.lineEdit().setReadOnly(True)
        self.received_date_input.setEnabled(False)
        calendar = self.received_date_input.calendarWidget()
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

        self.received_date_input.setFixedHeight(36)
        self.received_date_input.setStyleSheet("""
                            background-color: #f8fafc;
                            border: 1px solid #e2e8f0;
                            border-radius: 6px;
                            padding: 0 10px;
                            font-size: 14px;
                        """)

        row_two_middle_layout.addWidget(received_date_label)
        row_two_middle_layout.addWidget(self.received_date_input)

        row_two_right_layout = QVBoxLayout()
        row_two_right_layout.setSpacing(4)

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
                               padding: 4px 10px;
                               font-size: 14px;
                           }
                           QTextEdit:focus {
                                   border: 1px solid #4f46e5;
                               }
                       """)

        row_two_right_layout.addWidget(notes_label)
        row_two_right_layout.addWidget(self.notes_input)

        row_two_layout.addLayout(row_two_left_layout,1)
        row_two_layout.addLayout(row_two_middle_layout,1)
        row_two_layout.addLayout(row_two_right_layout,2)

        button_row_layout = QHBoxLayout()
        button_row_layout.setContentsMargins(0, 10, 0, 0)
        button_row_layout.setSpacing(12)

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

        self.submit_button = QPushButton("Add Income")
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

        self.submit_button.clicked.connect(self.handle_add_income)

        button_row_layout.addWidget(self.clear_button)
        button_row_layout.addWidget(self.submit_button)

        add_income_layout.addLayout(row_one_layout)
        add_income_layout.addLayout(row_two_layout)
        add_income_layout.addLayout(button_row_layout)
        add_income_layout.addStretch()

    def create_income_category_card(self,income_category,total_amount,details_data):

        card_box_frame = QFrame()
        card_box_frame.setStyleSheet("""QFrame {
                        background-color: white;
                        border-radius: 10px;
                    }
                """)
        card_box_frame.setFixedHeight(200)
        card_box_frame.setFixedWidth(225)

        card_box_frame_layout = QVBoxLayout()
        card_box_frame_layout.setContentsMargins(0, 10, 0, 10)
        card_box_frame_layout.setSpacing(8)

        card_box_frame.setLayout(card_box_frame_layout)

        income_category_label = QLabel(f"{income_category.title()} · £{total_amount}")
        income_category_label.setStyleSheet("""
                                    color: #334155;
                                    font-size: 16px;
                                    font-weight: 700;
                                """)
        income_category_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        separate_line = QFrame()
        separate_line.setFixedHeight(1)
        separate_line.setStyleSheet("""
            background-color: black;
            border: none;
        """)
        separate_line.setContentsMargins(0,0,0,0)

        card_box_frame_layout.addWidget(income_category_label)
        card_box_frame_layout.addSpacing(5)
        card_box_frame_layout.addWidget(separate_line)

        details_container = QWidget()
        details_layout = QVBoxLayout()
        details_container.setLayout(details_layout)
        details_container.setStyleSheet("""
                    background-color: transparent;;
                    border: none;
                """)



        if not details_data:
            no_data_label = QLabel("No income data available")
            no_data_label.setStyleSheet("""
                                    color: #334155;
                                    font-size: 13px;
                                    color: #64748b;
                                """)
            no_data_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            details_layout.addStretch()
            details_layout.addWidget(no_data_label)
            details_layout.addStretch()
            card_box_frame_layout.addWidget(details_container)

        else:
            for each_income_data in details_data:
                row_layout = QHBoxLayout()
                row_layout.setContentsMargins(0, 10, 0, 0)
                row_layout.setSpacing(4)

                row_button = QPushButton(
                    f"{each_income_data["source_name"]} : £{each_income_data["amount"]:,.2f}"
                )

                row_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

                row_button.setStyleSheet("""
                    QPushButton {
                        border: none;
                        background-color: transparent;
                        text-align: left;
                        padding: 4px 8px;
                        color: #334155;
                        font-size: 13px;
                        border-radius: 6px;
                    }

                    QPushButton:hover {
                        background-color: #eef2ff;
                        color: #4f46e5;
                    }

                    QPushButton:pressed {
                        background-color: #e0e7ff;
                    }
                """)

                row_button.clicked.connect(lambda checked=False, income_data = each_income_data:
                                           self.handle_updated_button_clicked(income_data))

                row_layout.addWidget(row_button)


                details_layout.addLayout(row_layout)

            details_layout.addStretch()
            card_box_frame_layout.addWidget(details_container)

        return card_box_frame


    def income_details_widget(self):
        self.details_container = QWidget()
        details_layout = QVBoxLayout()
        details_layout.setContentsMargins(0,20,0,0)
        details_layout.setSpacing(0)
        self.details_container.setLayout(details_layout)

        self.income_details_row_one_layout = QHBoxLayout()
        self.income_details_row_one_layout.setContentsMargins(0,0,0,0)
        self.income_details_row_one_layout.setSpacing(8)

        self.income_details_row_two_layout = QHBoxLayout()
        self.income_details_row_two_layout.setContentsMargins(0, 20, 0, 0)
        self.income_details_row_two_layout.setSpacing(8)


        details_layout.addLayout(self.income_details_row_one_layout )
        details_layout.addLayout(self.income_details_row_two_layout)

    def handle_is_recurring_value_changed(self):

        if self.income_frequency_input.currentData() == "one off":
            self.received_date_input.setEnabled(True)
        else:
            self.received_date_input.setEnabled(False)

    def handle_add_income(self):

        if not self.validate_expense_form():
            return

        received_date = None

        if self.income_frequency_input.currentData() == "one off":
            received_date = self.received_date_input.date().toString("yyyy-MM-dd")

        income_data = {
            "category":self.income_category_input.currentData(),
            "amount":self.amount_input.text(),
            "source_name":self.source_name_input.text(),
            "frequency":self.income_frequency_input.currentData(),
            "notes":self.notes_input.toPlainText().strip() or None,
            "received_date": received_date
        }

        try:

            add_income(income_data,self.get_access_token())
            info_message_box = MessageDialog("Success", "Income Added")
            info_message_box.success_dialog()
            info_message_box.exec()
            self.handle_clear_form()
            self.load_incomes_data()

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
        self.notes_input.setText("")
        self.source_name_input.setText("")

    def validate_expense_form(self):

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
            self.amount_error.setText("Amount Must Be A Valid Number")
            return False

        if amount <= 0:
            self.amount_error.setText("Amount Must Be Greater Than 0")
            return False

        if not source_name:
            self.source_name_error.setText("Shop Name Is Required")
            return False

        return True


    def load_incomes_data(self):

        if self.loading_finished:
            clear_layout(self.income_details_row_one_layout)
            clear_layout(self.income_details_row_two_layout)

        try:
            response = get_income_by_user_id(self.get_access_token())
            categorized_incomes_total = response["categorized_income_total"]
            incomes_details = response["incomes_details"]
            card_added = 0
            for each_income_category in ["salary", "bonus", "freelance", "benefits","rental income", "investment", "pension", "other"]:
                total_amount = 0
                each_income_details = None
                for each_categorized_income_total in categorized_incomes_total:
                    if each_income_category == each_categorized_income_total["category"]:
                        total_amount = each_categorized_income_total["total_amount"]

                for each_details in incomes_details:
                    if each_income_category == each_details["category"]:
                        each_income_details = each_details["data"]

                card_frame = self.create_income_category_card(each_income_category, str(f"{total_amount:,.2f}"), each_income_details)
                card_added += 1
                if card_added <= 4:
                    self.income_details_row_one_layout.addWidget(card_frame)
                else:
                    self.income_details_row_two_layout.addWidget(card_frame)

                self.loading_finished = True


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
                self.handle_token_expired()

            api_error_message_dialog = MessageDialog("API Error", str(error))

            api_error_message_dialog.error_dialog()

            api_error_message_dialog.exec()


    def handle_updated_button_clicked(self, income_data):

        update_income_dialog = EditIncomeDialog(self.handle_edit_income,self.handle_delete_income,income_data)
        update_income_dialog.exec()

    def handle_edit_income(self,income_id,income_data):
        try:
            update_income_by_income_id(income_id,self.get_access_token(),income_data)
            self.load_incomes_data()

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
                self.handle_token_expired()

            api_error_message_dialog = MessageDialog("API Error", str(error))

            api_error_message_dialog.error_dialog()

            api_error_message_dialog.exec()

    def handle_delete_income(self,income_id):
        try:
            delete_income_by_income_id(income_id, self.get_access_token())
            self.load_incomes_data()

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
                self.handle_token_expired()

            api_error_message_dialog = MessageDialog("API Error", str(error))

            api_error_message_dialog.error_dialog()

            api_error_message_dialog.exec()