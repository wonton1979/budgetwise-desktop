import requests
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QCursor, QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QHBoxLayout, QLabel, QProgressBar

from config import get_resource_directory
from services.savings_service import get_savings_by_user_id, add_new_savings, update_savings, delete_savings
from ui.components.dialogs.message_dialog import MessageDialog
from ui.savings.add_savings_dialog import AddSavingsDialog
from utils.clickable_frame import ClickableFrame
from ui.savings.edit_savings_dialog import EditSavingsDialog
from utils.clear_layout import clear_layout
from utils.date_format_convertor import uk_date_format, long_date_format


class SavingsPage(QWidget):
    def __init__(self,access_token_getter,handle_token_expired,currency_symbol,date_format):
        super().__init__()
        self.details_container = None
        self.get_access_token = access_token_getter
        self.handle_token_expired = handle_token_expired
        self.currency_symbol = currency_symbol
        self.date_format = date_format
        self.create_savings_page()
        self.loading_finished = False

    def create_savings_page(self):
        self.savings_page_layout = QVBoxLayout()
        self.savings_page_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.savings_page_layout)

        self.savings_cards_container()

        self.savings_page_layout.addWidget(self.details_container)

    def create_savings_details_card(self, savings_data):

        if savings_data:
            card_box_frame = ClickableFrame()
            card_box_frame.setObjectName("savingsCard")

            card_box_frame.setStyleSheet("""
                        QFrame#savingsCard {
                            background-color: white;
                            border: 1px solid #4f46e5;
                            border-radius: 6px;
                        }
                        QFrame#savingsCard:hover {
                            background-color: #eff6ff;
                            border: 2px solid #3b82f6;
                        }
                    """)
            card_box_frame.setFixedHeight(180)
            card_box_frame.setFixedWidth(225)
            card_box_frame.setCursor(QCursor(Qt.CursorShape.OpenHandCursor))
            card_box_frame.clicked.connect(lambda clicked=False,savings =savings_data :  self.handle_updated_button_clicked(savings))

            card_box_frame_layout = QVBoxLayout()
            card_box_frame_layout.setContentsMargins(0, 10, 0, 10)
            card_box_frame_layout.setSpacing(0)

            card_box_frame.setLayout(card_box_frame_layout)

            savings_name_label = QLabel(f"{savings_data["purpose_name"].title()}")
            savings_name_label.setStyleSheet("""   
                                                background-color: transparent;
                                                color: #334155;
                                                font-size: 12px;
                                                font-weight: 700;
                                            """)

            savings_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            separate_line = QFrame()
            separate_line.setFixedHeight(1)
            separate_line.setStyleSheet("""
                           background-color: #4f46e5;
                           border: none;
                       """)
            separate_line.setContentsMargins(0, 0, 0, 0)

            card_box_frame_layout.addWidget(savings_name_label)
            card_box_frame_layout.addSpacing(5)
            card_box_frame_layout.addWidget(separate_line)

            details_container = QWidget()
            details_layout = QVBoxLayout()
            details_container.setLayout(details_layout)
            details_container.setStyleSheet("""
                                   background-color: transparent;;
                                   border: none;
                               """)

            row_layout = QVBoxLayout()
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setSpacing(7)

            goal_amount = savings_data["goal_amount"]
            current_amount = savings_data["current_amount"]
            remaining_amount = goal_amount - current_amount

            target_amount_label = QLabel(f"Target:  {self.currency_symbol}{goal_amount:,.2f}")
            target_amount_label.setStyleSheet("""
                                                                       color: #334155;
                                                                       font-size: 12px;
                                                                       font-weight: 700;
                                                                   """)

            current_amount_label = QLabel(f"Saved:  {self.currency_symbol}{current_amount:,.2f}")
            current_amount_label.setStyleSheet("""
                                                                                   color: #334155;
                                                                                   font-size: 12px;
                                                                                   font-weight: 700;
                                                                               """)

            remaining_amount_label = QLabel(f"Remaining:  {self.currency_symbol}{remaining_amount:,.2f}")
            remaining_amount_label.setStyleSheet("""
                                                                                               color: #334155;
                                                                                               font-size: 12px;
                                                                                               font-weight: 700;
                                                                                           """)

            if current_amount > 0:
                progress = (current_amount / goal_amount) * 100
            else:
                progress = 0

            progress = min(progress, 100)

            if progress >= 100:
                chunk_color = "#22c55e"
            elif progress >= 20:
                chunk_color = "#4f46e5"
            else:
                chunk_color = "#94a3b8"

            progress_bar = QProgressBar()

            progress_bar.setValue(int(progress))

            progress_bar.setFormat(f"{progress:.1f}%")

            progress_bar.setStyleSheet(f"""
                        QProgressBar {{
                            border: none;
                            border-radius: 2px;
                            background-color: #94a3b8;
                            text-align: center;
                            height: 18px;
                            font-size: 12px;
                            color: white;
                            font-weight: 600;
                        }}

                        QProgressBar::chunk {{
                            background-color: {chunk_color};
                            border-radius: 8px;
                        }}
                    """)

            if savings_data["target_date"]:
                target_date_text = savings_data["target_date"]
                match self.date_format:
                    case "DD/MM/YYYY":
                        target_date_text = uk_date_format(str(savings_data["target_date"]))
                    case "DD MMM YYYY":
                        target_date_text = long_date_format(str(savings_data["target_date"]))

            else:
                target_date_text = "N/A"

            target_date_label = QLabel(f"Target Date: {target_date_text}")
            target_date_label.setStyleSheet("""
                                                color: #334155;
                                                font-size: 12px;
                                                font-weight: 700;
                                            """)

            row_layout.addWidget(target_amount_label)
            row_layout.addWidget(current_amount_label)
            row_layout.addWidget(remaining_amount_label)
            row_layout.addWidget(progress_bar)
            row_layout.addSpacing(5)
            row_layout.addWidget(target_date_label)

            details_layout.addLayout(row_layout)
            details_layout.addStretch()
            card_box_frame_layout.addWidget(details_container)

        else:
            card_box_frame = ClickableFrame()
            card_box_frame.setObjectName("savingsCard")

            card_box_frame.setStyleSheet("""
                                    QFrame#savingsCard {
                                        background-color: white;
                                        border: 1px solid #4f46e5;
                                        border-radius: 6px;
                                    }
                                    QFrame#savingsCard:hover {
                                        background-color: #eff6ff;
                                        border: 2px solid #3b82f6;
                                    }
                                """)
            card_box_frame.setFixedHeight(180)
            card_box_frame.setFixedWidth(225)
            card_box_frame.setCursor(QCursor(Qt.CursorShape.OpenHandCursor))
            card_box_frame.clicked.connect(self.show_add_savings_dialog)

            card_box_frame_layout = QVBoxLayout()
            card_box_frame_layout.setContentsMargins(0, 10, 0, 10)
            card_box_frame_layout.setSpacing(0)

            card_box_frame.setLayout(card_box_frame_layout)

            savings_name_label = QLabel("Add New Savings")
            savings_name_label.setStyleSheet("""   
                                                            background-color: transparent;
                                                            color: #334155;
                                                            font-size: 12px;
                                                            font-weight: 700;
                                                        """)

            savings_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            separate_line = QFrame()
            separate_line.setFixedHeight(1)
            separate_line.setStyleSheet("""
                                       background-color: #4f46e5;
                                       border: none;
                                   """)
            separate_line.setContentsMargins(0, 0, 0, 0)

            card_box_frame_layout.addWidget(savings_name_label)
            card_box_frame_layout.addSpacing(5)
            card_box_frame_layout.addWidget(separate_line)

            details_container = QWidget()
            details_layout = QVBoxLayout()
            details_container.setLayout(details_layout)
            details_container.setStyleSheet("""
                                               background-color: transparent;;
                                               border: none;
                                           """)

            row_layout = QVBoxLayout()
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setSpacing(7)



            add_new_savings_label = QLabel()
            icon_path = get_resource_directory()  / "icons" / "plus.png"
            add_new_savings_label.setPixmap(QIcon(str(icon_path)).pixmap(38, 38))
            add_new_savings_label.setAlignment(Qt.AlignmentFlag.AlignCenter)


            row_layout.addWidget(add_new_savings_label)
            details_layout.addStretch()
            details_layout.addLayout(row_layout)
            details_layout.addStretch()
            card_box_frame_layout.addWidget(details_container)

        return card_box_frame

    def savings_cards_container(self):
        self.details_container = QFrame()
        self.details_container.setStyleSheet("""background-color: white;""")
        self.setMinimumSize(300, 300)

        details_layout = QVBoxLayout()
        details_layout.setContentsMargins(0, 10, 0, 0)
        details_layout.setSpacing(0)
        self.details_container.setLayout(details_layout)

        self.savings_details_row_one_layout = QHBoxLayout()
        self.savings_details_row_one_layout.setContentsMargins(10, 20, 0, 0)
        self.savings_details_row_one_layout.setSpacing(8)

        self.savings_details_row_two_layout = QHBoxLayout()
        self.savings_details_row_two_layout.setContentsMargins(10, 20, 0, 0)
        self.savings_details_row_two_layout.setSpacing(8)

        self.savings_details_row_three_layout = QHBoxLayout()
        self.savings_details_row_three_layout.setContentsMargins(10, 20, 0, 0)
        self.savings_details_row_three_layout.setSpacing(8)

        details_layout.addLayout(self.savings_details_row_one_layout)
        details_layout.addLayout(self.savings_details_row_two_layout)
        details_layout.addLayout(self.savings_details_row_three_layout)
        details_layout.addStretch()

    def show_add_savings_dialog(self):
        self.add_savings_dialog = AddSavingsDialog(handle_add_savings=self.handle_add_savings,date_format=self.date_format)
        self.add_savings_dialog.exec()

    def handle_add_savings(self,savings_data):

        try:
            add_new_savings(savings_data, self.get_access_token())
            self.load_savings_data(self.currency_symbol)
            self.add_savings_dialog.add_savings_notify_label.setText("Added New Savings Successfully")
            QTimer.singleShot(2000, self.add_savings_dialog.reject)

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



    def load_savings_data(self,currency_symbol):

        clear_layout(self.savings_details_row_one_layout)
        clear_layout(self.savings_details_row_two_layout)

        try:
            response = get_savings_by_user_id(self.get_access_token())["data"]
            self.currency_symbol = currency_symbol
            total_savings_cards = 0
            if response:
                for i in range(len(response)):
                    if i < 3:
                        card_frame = self.create_savings_details_card(response[i])
                        self.savings_details_row_one_layout.addWidget(card_frame)
                    elif i< 6:
                        card_frame = self.create_savings_details_card(response[i])
                        self.savings_details_row_two_layout.addWidget(card_frame)
                    elif i< 9:
                        card_frame = self.create_savings_details_card(response[i])
                        self.savings_details_row_three_layout.addWidget(card_frame)
                    total_savings_cards += 1
                if total_savings_cards < 3:
                    card_frame = self.create_savings_details_card([])
                    self.savings_details_row_one_layout.addWidget(card_frame)
                elif 3 <= total_savings_cards <= 5:
                    card_frame = self.create_savings_details_card([])
                    self.savings_details_row_two_layout.addWidget(card_frame)
                elif 6 <= total_savings_cards <= 8:
                    card_frame = self.create_savings_details_card([])
                    self.savings_details_row_three_layout.addWidget(card_frame)


            else:
                card_frame = self.create_savings_details_card([])
                self.savings_details_row_one_layout.addWidget(card_frame)
                no_savings_label = QLabel("No savings goals yet.\n \nStart by creating your first savings target.")

                no_savings_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

                no_savings_label.setStyleSheet("""
                    color: #64748b;
                    font-size: 14px;
                    font-weight: 600;
                    padding: 30px;
                """)

                self.savings_details_row_two_layout.addWidget(no_savings_label)



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


    def handle_updated_button_clicked(self, savings_data):

        update_savings_dialog = EditSavingsDialog(self.handle_edit_savings, self.handle_delete_savings, savings_data,self.date_format)
        update_savings_dialog.exec()

    def handle_edit_savings(self, savings_id, updated_savings_data):
        try:
            update_savings(savings_id, updated_savings_data, self.get_access_token())
            self.load_savings_data(self.currency_symbol)

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

    def handle_delete_savings(self, savings_id):
        try:
            delete_savings(savings_id, self.get_access_token())
            self.load_savings_data(self.currency_symbol)

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

    def update_date_format(self,new_date_format):
        self.date_format = new_date_format