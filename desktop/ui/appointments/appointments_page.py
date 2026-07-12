import requests
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QFrame, QLabel

from services.appointment_service import add_appointment, get_appointments, update_appointment,delete_appointment
from ui.appointments.appointments_table import AppointmentTable
from ui.appointments.add_appointment_dialog import AddAppointmentsDialog
from ui.components.dialogs.message_dialog import MessageDialog


class AppointmentsPage(QWidget):

    def __init__(self,access_token_getter,handle_token_expired,date_format):
        super().__init__()
        self.get_access_token = access_token_getter
        self.handle_token_expired = handle_token_expired
        self.date_format = date_format
        self.setup_ui()


    def setup_ui(self):
        page_layout = QVBoxLayout()
        page_layout.setContentsMargins(0,0,0,0)
        page_layout.setSpacing(10)
        self.setStyleSheet("""
                    background-color: white;
                    border-radius: 10px;
                """)
        self.setLayout(page_layout)

        self.appointment_main_frame = QFrame()
        self.appointment_main_frame.setStyleSheet("""
                    background-color: white;
                    border-radius: 10px;
                """)

        appointment_main_frame_layout = QVBoxLayout()
        appointment_main_frame_layout.setContentsMargins(10, 10, 10, 10)
        self.appointment_main_frame.setLayout(appointment_main_frame_layout)

        self.add_appointment_dialog = AddAppointmentsDialog(self.handle_create_appointment,self.date_format)

        appointment_tab_widget = QTabWidget()
        appointment_tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                top: -1px;
            }

            QTabBar::tab {
                background: #1e293b;
                color: #ffffff;
                padding: 8px 16px;
                margin-right: 4px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }

            QTabBar::tab:selected {
                background: #ffffff;
                color: #000000;
                font-weight: 600;
            }

            QTabBar::tab:!selected:hover {
                background: #334155;
                color: #ffffff;
            }
        """)

        self.upcoming_appointments_table = AppointmentTable(self.handle_edit_appointment,
                                                            self.handle_delete_appointment,self.date_format)

        self.completed_appointments_table = AppointmentTable(self.handle_edit_appointment,
                                                             self.handle_delete_appointment,self.date_format)

        self.cancelled_appointments_table = AppointmentTable(self.handle_edit_appointment,
                                                             self.handle_delete_appointment,self.date_format)
        self.missed_or_expired_appointments_table = AppointmentTable(self.handle_edit_appointment,
                                                             self.handle_delete_appointment,self.date_format)

        appointment_tab_widget.addTab(self.upcoming_appointments_table, "Upcoming Appointments")
        appointment_tab_widget.addTab(self.completed_appointments_table, "Completed Appointments")
        appointment_tab_widget.addTab(self.cancelled_appointments_table, "Cancelled Appointments")
        appointment_tab_widget.addTab(self.missed_or_expired_appointments_table, "Missed or Expired Appointments")

        self.no_record_found_info_label = QLabel("")

        self.no_record_found_info_label.setStyleSheet("color: #4f46e5;font-size: 12px; font-weight: 600;")

        appointment_main_frame_layout.addWidget(appointment_tab_widget)
        appointment_main_frame_layout.addWidget(self.no_record_found_info_label)

        page_layout.addWidget(self.appointment_main_frame)


    def handle_create_appointment(self,appointment_details):
        try:
            add_appointment(appointment_details, self.get_access_token())
            self.add_appointment_dialog.form_message_label.setStyleSheet("color: #22c55e;font-size: 14px;")
            self.add_appointment_dialog.form_message_label.setText("New Appointment Added Successfully")
            QTimer.singleShot(2000, self.add_appointment_dialog.reject)
            self.load_appointments()

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

    def load_appointments(self,new_date_format=None):

        try:
            appointments_data = get_appointments(self.get_access_token())["data"]
            if new_date_format:
                self.upcoming_appointments_table.load_appointment_data(appointments_data["upcoming_appointments"],new_date_format)
                self.completed_appointments_table.load_appointment_data(appointments_data["completed_appointments"],new_date_format)
                self.cancelled_appointments_table.load_appointment_data(appointments_data["cancelled_appointments"],new_date_format)
                self.missed_or_expired_appointments_table.load_appointment_data(
                    appointments_data["expired_and_missed_appointments"],new_date_format)
            else:
                self.upcoming_appointments_table.load_appointment_data(appointments_data["upcoming_appointments"])
                self.completed_appointments_table.load_appointment_data(appointments_data["completed_appointments"])
                self.cancelled_appointments_table.load_appointment_data(appointments_data["cancelled_appointments"])
                self.missed_or_expired_appointments_table.load_appointment_data(
                    appointments_data["expired_and_missed_appointments"])

        except requests.ConnectionError:

            connection_error_message_dialog = MessageDialog("Connection Error", "Unable to connect to the server.")

            connection_error_message_dialog.error_dialog()

            connection_error_message_dialog.exec()


        except requests.Timeout:

            timeout_error_message_dialog = MessageDialog("Connection Error", "The request timed out.")

            timeout_error_message_dialog.error_dialog()

            timeout_error_message_dialog.exec()


        except Exception as error:

            if str(error) == "No appointments found":
                self.no_record_found_info_label.setText("No appointment yet. Add your first appointment to get started.")
                return

            if str(error) == "Session Expired":
                self.handle_token_expired()
                return

            api_error_message_dialog = MessageDialog("API Error", str(error))

            api_error_message_dialog.error_dialog()

            api_error_message_dialog.exec()

    def handle_edit_appointment(self,updated_appointment,appointment_id):

        try:
            update_appointment(updated_appointment,appointment_id, self.get_access_token())
            self.load_appointments()

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
                return

            api_error_message_dialog = MessageDialog("API Error", str(error))

            api_error_message_dialog.error_dialog()

            api_error_message_dialog.exec()


    def handle_delete_appointment(self,appointment_id):
        try:

            delete_appointment(appointment_id, self.get_access_token())
            self.load_appointments()

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
                return 

            api_error_message_dialog = MessageDialog("API Error", str(error))

            api_error_message_dialog.error_dialog()

            api_error_message_dialog.exec()

    def update_date_format(self,new_date_format):
        self.date_format =new_date_format
