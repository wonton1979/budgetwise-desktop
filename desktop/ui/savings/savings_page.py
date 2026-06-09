import requests
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QHBoxLayout, QLabel, QLineEdit, QTextEdit, \
    QPushButton, QDateEdit, QProgressBar

from services.savings_service import get_savings_by_user_id, add_new_savings, update_savings, delete_savings
from ui.components.dialogs.message_dialog import MessageDialog
from ui.savings.clickable_frame import ClickableFrame
from ui.savings.edit_savings_dialog import EditSavingsDialog
from utils.clear_layout import clear_layout
from utils.uk_date_format import uk_date_format


class SavingsPage(QWidget):
    def __init__(self,access_token_getter,handle_token_expired):
        super().__init__()
        self.details_container = None
        self.get_access_token = access_token_getter
        self.handle_token_expired = handle_token_expired

        self.create_savings_page()
        self.loading_finished = False

    def create_savings_page(self):
        self.savings_page_layout = QVBoxLayout()
        self.savings_page_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.savings_page_layout)

        self.add_savings_frame()
        self.savings_cards_container()

        self.savings_page_layout.addWidget(self.add_savings_card)
        self.savings_page_layout.addWidget(self.details_container)

    def add_savings_frame(self):
        self.add_savings_card = QFrame()
        self.add_savings_card.setStyleSheet("""
                       QFrame {
                           background-color: white;
                           border-radius: 10px;
                       }
                   """)
        self.add_savings_card.setFixedHeight(230)

        add_savings_layout = QVBoxLayout()
        add_savings_layout.setContentsMargins(10, 10, 10, 10)
        add_savings_layout.setSpacing(4)
        self.add_savings_card.setLayout(add_savings_layout)

        row_one_layout = QHBoxLayout()
        row_one_layout.setContentsMargins(0, 10, 0, 0)
        row_one_layout.setSpacing(8)

        row_one_left_layout = QVBoxLayout()
        row_one_left_layout.setSpacing(4)

        savings_name_label_layout = QHBoxLayout()
        savings_name_label_layout.setSpacing(4)

        savings_name_label = QLabel("Savings Name")
        savings_name_label.setStyleSheet("""
                                             color: #334155;
                                             font-size: 13px;
                                         """)

        self.savings_name_error = QLabel("")
        self.savings_name_error.setStyleSheet("""
                                                      color: #ef4444;
                                                      font-size: 10px;
                                                  """)

        savings_name_label_layout.addWidget(savings_name_label)
        savings_name_label_layout.addWidget(self.savings_name_error)

        self.savings_name_input = QLineEdit()
        self.savings_name_input.setPlaceholderText("Enter Savings Name")
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


        row_one_left_layout.addLayout(savings_name_label_layout)
        row_one_left_layout.addWidget(self.savings_name_input)

        row_one_middle_layout = QVBoxLayout()
        row_one_middle_layout.setSpacing(4)

        goal_amount_label_layout = QHBoxLayout()
        goal_amount_label_layout.setSpacing(4)

        goal_amount_label = QLabel("Target Amount (£)")
        goal_amount_label.setStyleSheet("""
                                            color: #334155;
                                            font-size: 13px;
                                        """)

        self.goal_amount_error = QLabel("")
        self.goal_amount_error.setStyleSheet("""
                                                     color: #ef4444;
                                                     font-size: 10px;
                                                 """)

        goal_amount_label_layout.addWidget(goal_amount_label)
        goal_amount_label_layout.addWidget(self.goal_amount_error)

        self.goal_amount_input = QLineEdit()
        self.goal_amount_input.setPlaceholderText("Enter Amount")
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

        row_one_middle_layout.addLayout(goal_amount_label_layout)
        row_one_middle_layout.addWidget(self.goal_amount_input)

        row_one_right_layout = QVBoxLayout()
        row_one_right_layout.setSpacing(4)

        target_date_label = QLabel("Target Date")
        target_date_label.setStyleSheet("""
                                  color: #334155;
                                  font-size: 13px;
                              """)
        tomorrow = QDate.currentDate().addDays(1)
        self.target_date_input = QDateEdit()
        self.target_date_input.setMinimumDate(tomorrow)
        self.target_date_input.setSpecialValueText("No Target Date")
        self.target_date_input.setDate(self.target_date_input.minimumDate())
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

        row_one_right_layout.addWidget(target_date_label)
        row_one_right_layout.addWidget(self.target_date_input)

        row_one_layout.addLayout(row_one_left_layout, 1)
        row_one_layout.addLayout(row_one_middle_layout, 1)
        row_one_layout.addLayout(row_one_right_layout, 1)

        row_two_layout = QHBoxLayout()
        row_two_layout.setContentsMargins(0, 10, 0, 0)
        row_two_layout.setSpacing(8)

        row_two_left_layout = QVBoxLayout()
        row_two_left_layout.setSpacing(4)

        current_amount_label_layout = QHBoxLayout()
        current_amount_label_layout.setSpacing(4)

        current_amount_label = QLabel("Current Amount (£)")
        current_amount_label.setStyleSheet("""
                                                    color: #334155;
                                                    font-size: 13px;
                                                """)

        self.current_amount_error = QLabel("")
        self.current_amount_error.setStyleSheet("""
                                                             color: #ef4444;
                                                             font-size: 10px;
                                                         """)

        current_amount_label_layout.addWidget(current_amount_label)
        current_amount_label_layout.addWidget(self.current_amount_error)

        self.current_amount_input = QLineEdit()
        self.current_amount_input.setText("0.00")
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

        row_two_left_layout.addLayout(current_amount_label_layout)
        row_two_left_layout.addWidget(self.current_amount_input)

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

        row_two_layout.addLayout(row_two_left_layout, 1)
        row_two_layout.addLayout(row_two_right_layout, 2)

        button_row_layout = QHBoxLayout()
        button_row_layout.setContentsMargins(0, 20, 0, 0)
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

        self.submit_button = QPushButton("Add Savings")
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

        self.submit_button.clicked.connect(self.handle_add_savings)

        button_row_layout.addWidget(self.clear_button)
        button_row_layout.addWidget(self.submit_button)

        add_savings_layout.addLayout(row_one_layout)
        add_savings_layout.addLayout(row_two_layout)
        add_savings_layout.addLayout(button_row_layout)
        add_savings_layout.addStretch()

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

            target_amount_label = QLabel(f"Target: £{goal_amount:,.2f}")
            target_amount_label.setStyleSheet("""
                                                                       color: #334155;
                                                                       font-size: 12px;
                                                                       font-weight: 700;
                                                                   """)

            current_amount_label = QLabel(f"Saved: £{current_amount:,.2f}")
            current_amount_label.setStyleSheet("""
                                                                                   color: #334155;
                                                                                   font-size: 12px;
                                                                                   font-weight: 700;
                                                                               """)

            remaining_amount_label = QLabel(f"Remaining: £{remaining_amount:,.2f}")
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
                target_date_text = uk_date_format(savings_data["target_date"])
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
            card_box_frame = QFrame()

            card_box_frame.setStyleSheet("""
                                    QFrame#savingsCard {
                                        background-color: white;
                                    }
                                """)
            card_box_frame.setFixedHeight(180)
            card_box_frame.setFixedWidth(225)

            card_box_frame_layout = QVBoxLayout()
            card_box_frame_layout.setContentsMargins(0, 10, 0, 10)
            card_box_frame_layout.setSpacing(0)

            card_box_frame.setLayout(card_box_frame_layout)

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
        self.savings_details_row_one_layout.setContentsMargins(10, 0, 0, 0)
        self.savings_details_row_one_layout.setSpacing(8)

        self.savings_details_row_two_layout = QHBoxLayout()
        self.savings_details_row_two_layout.setContentsMargins(10, 10, 0, 0)
        self.savings_details_row_two_layout.setSpacing(8)

        details_layout.addLayout(self.savings_details_row_one_layout)
        details_layout.addLayout(self.savings_details_row_two_layout)

    def handle_add_savings(self):

        if not self.validate_add_savings_form():
            return

        savings_data = {
            "purpose_name": self.savings_name_input.text().strip(),
            "goal_amount": float(self.goal_amount_input.text()),
            "current_amount": float(self.current_amount_input.text()),
            "target_date": self.target_date_input.date().toString("yyyy-MM-dd") if self.target_date_input.date() != self.target_date_input.minimumDate() else None,
            "notes": self.notes_input.toPlainText().strip() or None
        }

        try:

            add_new_savings(savings_data, self.get_access_token())
            info_message_box = MessageDialog("Success", "Savings Added")
            info_message_box.information_dialog()
            info_message_box.exec_()
            self.goal_amount_input.setText("")
            self.notes_input.setText("")
            self.savings_name_input.setText("")
            self.current_amount_input.setText("0.00")
            self.load_savings_data()


        except requests.ConnectionError:

            connection_error_message_dialog = MessageDialog("Connection Error", "Unable to connect to the server.")

            connection_error_message_dialog.error_dialog()

            connection_error_message_dialog.exec_()


        except requests.Timeout:

            timeout_error_message_dialog = MessageDialog("Connection Error", "The request timed out.")

            timeout_error_message_dialog.error_dialog()

            timeout_error_message_dialog.exec_()


        except Exception as error:

            api_error_message_dialog = MessageDialog("API Error", str(error))

            api_error_message_dialog.error_dialog()

            api_error_message_dialog.exec_()

            if str(error) == "Session Expired":
                self.handle_token_expired()

    def handle_clear_form(self):
        self.savings_name_input.setText("")
        self.goal_amount_input.setText("")
        self.current_amount_input.setText("0.00")
        self.notes_input.setPlainText("")

    def validate_add_savings_form(self):

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

        if goal_amount <= 0 :
            self.goal_amount_error.setText("Amount Must Be Greater Than Zero")
            return False

        if current_amount < 0 :
            self.current_amount_error.setText("Amount Can't Be Negative")
            return False

        if not savings_name:
            self.savings_name_error.setText("Savings Name Is Required")
            return False

        return True

    def load_savings_data(self):

        clear_layout(self.savings_details_row_one_layout)
        clear_layout(self.savings_details_row_two_layout)

        try:
            response = get_savings_by_user_id(self.get_access_token())["data"]

            if response:
                for i in range(6):
                    if len(response) >= i+1:
                        card_frame = self.create_savings_details_card(response[i])
                    else:
                        card_frame = self.create_savings_details_card([])
                    if i<=2:
                        self.savings_details_row_one_layout.addWidget(card_frame)
                    else:
                        self.savings_details_row_two_layout.addWidget(card_frame)
            else:
                no_savings_label = QLabel("No savings goals yet.\n \nStart by creating your first savings target.")

                no_savings_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

                no_savings_label.setStyleSheet("""
                    color: #64748b;
                    font-size: 14px;
                    font-weight: 600;
                    padding: 30px;
                """)

                self.savings_details_row_one_layout.addWidget(no_savings_label)



        except requests.ConnectionError:

            connection_error_message_dialog = MessageDialog("Connection Error", "Unable to connect to the server.")

            connection_error_message_dialog.error_dialog()

            connection_error_message_dialog.exec_()


        except requests.Timeout:

            timeout_error_message_dialog = MessageDialog("Connection Error", "The request timed out.")

            timeout_error_message_dialog.error_dialog()

            timeout_error_message_dialog.exec_()


        except Exception as error:

            api_error_message_dialog = MessageDialog("API Error", str(error))

            api_error_message_dialog.error_dialog()

            api_error_message_dialog.exec_()

            if str(error) == "Session Expired":
                self.handle_token_expired()


    def handle_updated_button_clicked(self, savings_data):

        update_savings_dialog = EditSavingsDialog(self.handle_edit_savings, self.handle_delete_savings, savings_data)
        update_savings_dialog.exec_()

    def handle_edit_savings(self, savings_id, updated_savings_data):
        try:
            update_savings(savings_id, updated_savings_data, self.get_access_token())
            self.load_savings_data()

        except requests.ConnectionError:

            connection_error_message_dialog = MessageDialog("Connection Error", "Unable to connect to the server.")

            connection_error_message_dialog.error_dialog()

            connection_error_message_dialog.exec_()

        except requests.Timeout:

            timeout_error_message_dialog = MessageDialog("Connection Error", "The request timed out.")

            timeout_error_message_dialog.error_dialog()

            timeout_error_message_dialog.exec_()

        except Exception as error:

            api_error_message_dialog = MessageDialog("API Error", str(error))

            api_error_message_dialog.error_dialog()

            api_error_message_dialog.exec_()

            if str(error) == "Session Expired":
                self.handle_token_expired()

    def handle_delete_savings(self, savings_id):
        try:
            delete_savings(savings_id, self.get_access_token())
            self.load_savings_data()

        except requests.ConnectionError:

            connection_error_message_dialog = MessageDialog("Connection Error", "Unable to connect to the server.")

            connection_error_message_dialog.error_dialog()

            connection_error_message_dialog.exec_()

        except requests.Timeout:

            timeout_error_message_dialog = MessageDialog("Connection Error", "The request timed out.")

            timeout_error_message_dialog.error_dialog()

            timeout_error_message_dialog.exec_()

        except Exception as error:

            api_error_message_dialog = MessageDialog("API Error", str(error))

            api_error_message_dialog.error_dialog()

            api_error_message_dialog.exec_()

            if str(error) == "Session Expired":
                self.handle_token_expired()