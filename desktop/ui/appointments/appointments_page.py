import requests
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QFrame, QLabel

from services.appointment_service import add_appointment, get_appointments, update_appointment,delete_appointment
from ui.appointments.appointments_table import AppointmentTable
from ui.appointments.create_appointment import AppointmentsCard
from ui.components.dialogs.message_dialog import MessageDialog


class AppointmentsPage(QWidget):

    def __init__(self,access_token_getter,handle_token_expired):
        super().__init__()
        self.get_access_token = access_token_getter
        self.handle_token_expired = handle_token_expired
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

        self.add_appointment_card = AppointmentsCard(self.get_access_token, self.handle_token_expired,
                                                     self.handle_create_appointment)

        appointment_tab_widget = QTabWidget()
        appointment_tab_widget.setStyleSheet("""
        
            QTabWidget {
                background-color: #1e293b;
                
            }
            
            QTabWidget::pane {
                background-color: white;
                border: 1px solid #cbd5e1;
                top: 0px;
            }
        
            QTabBar::tab {
                background: #e2e8f0;
                color: #334155;
                padding: 8px 16px;
                
                border: 1px solid #cbd5e1;
                border-bottom: none;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }
            
            QTabBar::tab:selected {
                background: #e2e8f0;
                color: #0f172a;
                font-weight: 600;
            }
        """)

        self.upcoming_appointments_table = AppointmentTable(self.handle_edit_appointment,
                                                            self.handle_delete_appointment)

        self.completed_appointments_table = AppointmentTable(self.handle_edit_appointment,
                                                             self.handle_delete_appointment)

        self.cancelled_appointments_table = AppointmentTable(self.handle_edit_appointment,
                                                             self.handle_delete_appointment)
        self.missed_or_expired_appointments_table = AppointmentTable(self.handle_edit_appointment,
                                                             self.handle_delete_appointment)

        appointment_tab_widget.addTab(self.upcoming_appointments_table, "Upcoming Appointments")
        appointment_tab_widget.addTab(self.completed_appointments_table, "Completed Appointments")
        appointment_tab_widget.addTab(self.cancelled_appointments_table, "Cancelled Appointments")
        appointment_tab_widget.addTab(self.missed_or_expired_appointments_table, "Missed or Expired Appointments")

        self.no_record_found_info_label = QLabel("")

        self.no_record_found_info_label.setStyleSheet("color: #4f46e5;font-size: 12px; font-weight: 600;")

        appointment_main_frame_layout.addWidget(self.add_appointment_card)
        appointment_main_frame_layout.addWidget(appointment_tab_widget)
        appointment_main_frame_layout.addWidget(self.no_record_found_info_label)

        page_layout.addWidget(self.appointment_main_frame)


    def handle_create_appointment(self,appointment_details):
        try:
            add_appointment(appointment_details, self.get_access_token())
            add_appointment_success_dialog = MessageDialog(message_title="Information",
                                                      message_content="Appointment successfully added!")
            add_appointment_success_dialog.success_dialog()
            add_appointment_success_dialog.exec()

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

    def load_appointments(self):

        try:
            appointments_data = get_appointments(self.get_access_token())["data"]

            self.upcoming_appointments_table.create_appointment_list_table(appointments_data["upcoming_appointments"])
            self.completed_appointments_table.create_appointment_list_table(appointments_data["completed_appointments"])
            self.cancelled_appointments_table.create_appointment_list_table(appointments_data["cancelled_appointments"])
            self.missed_or_expired_appointments_table.create_appointment_list_table(appointments_data["expired_and_missed_appointments"])

        except requests.ConnectionError:

            connection_error_message_dialog = MessageDialog("Connection Error", "Unable to connect to the server.")

            connection_error_message_dialog.error_dialog()

            connection_error_message_dialog.exec()


        except requests.Timeout:

            timeout_error_message_dialog = MessageDialog("Connection Error", "The request timed out.")

            timeout_error_message_dialog.error_dialog()

            timeout_error_message_dialog.exec()


        except Exception as error:

            if str(error) == "Resource Not Found":
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

