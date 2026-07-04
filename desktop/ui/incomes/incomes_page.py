import requests
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QHBoxLayout, QLabel, QPushButton

from services.income_service import add_income, get_income_by_user_id, update_income_by_income_id, \
    delete_income_by_income_id
from ui.components.dialogs.message_dialog import MessageDialog
from ui.incomes.add_income_dialog import AddIncomeDialog
from ui.incomes.edit_income_dialog import EditIncomeDialog
from utils.clear_layout import clear_layout



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
        self.incomes_page_layout.setContentsMargins(0, 0, 0, 10)
        self.setLayout(self.incomes_page_layout)

        self.add_income_dialog = AddIncomeDialog(self.handle_add_income)
        self.income_details_widget()

        self.incomes_page_layout.addWidget(self.details_container)



    def create_income_category_card(self,income_category,total_amount,details_data):

        card_box_frame = QFrame()
        card_box_frame.setStyleSheet("""QFrame {
                        background-color: white;
                        border-radius: 10px;
                    }
                """)
        card_box_frame.setFixedHeight(200)
        card_box_frame.setFixedWidth(280)

        card_box_frame_layout = QVBoxLayout()
        card_box_frame_layout.setContentsMargins(0, 10, 0, 10)
        card_box_frame_layout.setSpacing(5)

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

        self.income_details_row_three_layout = QHBoxLayout()
        self.income_details_row_three_layout.setContentsMargins(0, 20, 0, 0)
        self.income_details_row_three_layout.setSpacing(8)


        details_layout.addLayout(self.income_details_row_one_layout )
        details_layout.addLayout(self.income_details_row_two_layout)
        details_layout.addLayout(self.income_details_row_three_layout)



    def handle_add_income(self,income_data):

        try:
            add_income(income_data,self.get_access_token())
            self.add_income_dialog.add_income_notify_label.setText("Income Added Successfully")
            QTimer.singleShot(2000, self.add_income_dialog.reject)
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


    def load_incomes_data(self):

        if self.loading_finished:
            clear_layout(self.income_details_row_one_layout)
            clear_layout(self.income_details_row_two_layout)
            clear_layout(self.income_details_row_three_layout)

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
                if card_added <= 3:
                    self.income_details_row_one_layout.addWidget(card_frame)
                elif card_added <= 6:
                    self.income_details_row_two_layout.addWidget(card_frame)
                else:
                    self.income_details_row_three_layout.addWidget(card_frame)

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