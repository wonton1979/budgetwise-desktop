import requests
from PySide6.QtWidgets import QWidget, QVBoxLayout

from services.memorable_day_service import add_memorable_day,get_memorable_days,patch_memorable_day,delete_memorable_day
from ui.components.dialogs.message_dialog import MessageDialog
from ui.memorable_days.memorable_day_main_frame import MemorableDaysFrame
from utils.clear_layout import clear_layout


class MemorableDayPage(QWidget):

    def __init__(self,access_token_getter,handle_token_expired,date_format):
        super().__init__()
        self.get_access_token = access_token_getter
        self.handle_token_expired = handle_token_expired
        self.date_format = date_format
        memorable_day_layout = QVBoxLayout()
        memorable_day_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(memorable_day_layout)
        self.main_frame = MemorableDaysFrame(self.handle_add_memorable_day,self.handle_update_memorable_day,
                                             self.handle_delete_memorable_day,
                                             self.date_format)
        memorable_day_layout.addWidget(self.main_frame)

    def handle_add_memorable_day(self,memorable_day_data):
        try:
            add_memorable_day(memorable_day_data,self.get_access_token())
            self.load_memorable_days()

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

    def handle_update_memorable_day(self,memorable_day_data,memorable_day_id):
        try:
            patch_memorable_day(self.get_access_token(),memorable_day_data,memorable_day_id)
            self.load_memorable_days()

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

    def handle_delete_memorable_day(self, memorable_day_id):

        try:
            delete_memorable_day(self.get_access_token(),memorable_day_id)
            self.load_memorable_days()

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

    def load_memorable_days(self):
        clear_layout(self.main_frame.memorable_cards_row_one_layout)
        clear_layout(self.main_frame.memorable_cards_row_two_layout)
        clear_layout(self.main_frame.memorable_cards_row_three_layout)
        try:
            response = get_memorable_days(self.get_access_token())
            total_cards = 0
            if len(response["data"]) > 0:
                for each_memorable_day in response["data"]:
                    if total_cards <= 3:
                        self.main_frame.memorable_cards_row_one_layout.addWidget(
                            self.main_frame.create_memorable_day_details_card(each_memorable_day,self.date_format))
                    if 3 < total_cards <= 7:
                        self.main_frame.memorable_cards_row_two_layout.addWidget(
                            self.main_frame.create_memorable_day_details_card(each_memorable_day))
                    if 8 < total_cards <= 11:
                        self.main_frame.memorable_cards_row_three_layout.addWidget(
                            self.main_frame.create_memorable_day_details_card(each_memorable_day))
                    total_cards = total_cards + 1
                if total_cards <= 3:
                    self.main_frame.memorable_cards_row_one_layout.addWidget(self.main_frame.add_memorable_day_card())
                if 3 < total_cards <= 7:
                    self.main_frame.memorable_cards_row_two_layout.addWidget(self.main_frame.add_memorable_day_card())
                if 8 < total_cards <= 11:
                    self.main_frame.memorable_cards_row_three_layout.addWidget(self.main_frame.add_memorable_day_card())
            else:
                self.main_frame.memorable_cards_row_one_layout.addWidget(self.main_frame.add_memorable_day_card())
                self.main_frame.memorable_cards_row_one_layout.addStretch()


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


    def update_date_format(self,new_date_format):
        self.date_format = new_date_format

