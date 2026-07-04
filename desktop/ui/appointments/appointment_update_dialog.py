from PySide6.QtCore import QTimer, QDate, QTime
from PySide6.QtWidgets import QDialog, QFrame, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QLineEdit, \
    QTextEdit, QPushButton, QMessageBox, QDateEdit, QTimeEdit, QComboBox

from utils.combobox_style import get_combo_style
from utils.date_picker_style import get_date_picker_style


class AppointmentUpdateDialog(QDialog):
    def __init__(self, handle_edit_appointment_record, handle_delete_appointment_record, existing_appointment_record):
        super().__init__()
        self.setWindowTitle("Update Appointment")
        self.setModal(True)
        self.resize(660, 330)
        self.handle_edit_appointment_record = handle_edit_appointment_record
        self.handle_delete_appointment_record = handle_delete_appointment_record
        self.existing_payload = existing_appointment_record
        self.create_edit_appointment_card()
        self.load_existing_payload()

    def create_edit_appointment_card(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(8, 8, 8, 8)
        self.setLayout(main_layout)

        self.edit_appointment_card = QFrame()
        self.edit_appointment_card.setStyleSheet("""
            background-color: white;
            border-radius: 10px;
        """)

        edit_appointment_card_layout = QVBoxLayout()
        self.edit_appointment_card.setLayout(edit_appointment_card_layout)
        edit_appointment_card_layout.setContentsMargins(20, 20, 20, 20)
        edit_appointment_card_layout.setSpacing(12)

        row_one_layout = QHBoxLayout()
        row_one_layout.setSpacing(12)
        row_one_layout.setContentsMargins(0, 0, 0, 0)

        row_one_left_layout = QVBoxLayout()
        row_one_left_layout.setSpacing(4)

        date_label = QLabel("Appointment Date")
        date_label.setStyleSheet("""
                           color: #334155;
                           font-size: 13px;
                       """)

        self.date_input = QDateEdit()

        self.date_input.setCalendarPopup(True)
        self.date_input.setMinimumDate(QDate.currentDate())
        self.date_input.setDate(QDate.currentDate())
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


        row_one_left_layout.addWidget(date_label)
        row_one_left_layout.addWidget(self.date_input)

        row_one_right_layout = QVBoxLayout()
        row_one_right_layout.setSpacing(4)

        appointment_time_label = QLabel("Appointment Time")
        appointment_time_label.setStyleSheet("""
                                                                          color: #334155;
                                                                          font-size: 13px;
                                                                      """)

        self.appointment_time_input = QTimeEdit()
        self.appointment_time_input.setDisplayFormat("HH:mm")
        self.appointment_time_input.setTime(QTime.currentTime())
        self.appointment_time_input.setStyleSheet("""
                                    QTimeEdit {
                                        background-color: #f8fafc;
                                        border: 1px solid #e2e8f0;
                                        border-radius: 6px;
                                        padding: 0 10px;
                                        font-size: 14px;
                                    }

                                    QTimeEdit:focus {
                                        border: 1px solid #4f46e5;
                                    }
                                """)
        self.appointment_time_input.setFixedHeight(36)

        row_one_right_layout.addWidget(appointment_time_label)
        row_one_right_layout.addWidget(self.appointment_time_input)

        row_one_layout.addLayout(row_one_left_layout, 1)
        row_one_layout.addLayout(row_one_right_layout,1)



        row_two_layout = QHBoxLayout()
        row_two_layout.setSpacing(12)
        row_two_layout.setContentsMargins(0, 0, 0, 0)

        row_two_left_layout = QVBoxLayout()
        row_two_left_layout.setSpacing(4)

        contact_label = QLabel("Contact Name")
        contact_label.setStyleSheet("""
                                    color: #334155;
                                    font-size: 13px;
                                """)

        self.contact_input = QLineEdit()
        self.contact_input.setPlaceholderText("Person or organisation")
        self.contact_input.setFixedHeight(36)
        self.contact_input.setStyleSheet("""
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

        row_two_left_layout.addWidget(contact_label)
        row_two_left_layout.addWidget(self.contact_input)

        row_two_right_layout = QVBoxLayout()
        row_two_right_layout.setSpacing(4)

        purpose_label = QLabel("Purpose of Appointment")
        purpose_label.setStyleSheet("""
                                            color: #334155;
                                            font-size: 13px;
                                        """)

        self.purpose_input = QLineEdit()
        self.purpose_input.setPlaceholderText("Parents' Evening, Interview")
        self.purpose_input.setFixedHeight(36)
        self.purpose_input.setStyleSheet("""
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

        row_two_right_layout.addWidget(purpose_label)
        row_two_right_layout.addWidget(self.purpose_input)

        row_two_layout.addLayout(row_two_left_layout, 1)
        row_two_layout.addLayout(row_two_right_layout, 1)

        row_three_layout = QHBoxLayout()
        row_three_layout.setSpacing(12)
        row_three_layout.setContentsMargins(0, 0, 0, 0)

        row_three_left_layout = QVBoxLayout()
        row_three_left_layout.setSpacing(4)

        appointment_type_label = QLabel("Type of Appointment")
        appointment_type_label.setStyleSheet("""
                                    color: #334155;
                                    font-size: 13px;
                                """)

        self.appointment_type_input = QComboBox()
        self.appointment_type_input.setMaxVisibleItems(8)
        self.appointment_type_input.addItem("In Person", "in person")
        self.appointment_type_input.addItem("Online", "online")

        self.appointment_type_input.setFixedHeight(36)
        self.appointment_type_input.setStyleSheet(get_combo_style())

        row_three_left_layout.addWidget(appointment_type_label)
        row_three_left_layout.addWidget(self.appointment_type_input)

        row_three_right_layout = QVBoxLayout()
        row_three_right_layout.setSpacing(4)

        location_label = QLabel("Location")
        location_label.setStyleSheet("""
                                                    color: #334155;
                                                    font-size: 13px;
                                                """)

        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText("Appointment Address")
        self.location_input.setFixedHeight(36)
        self.location_input.setStyleSheet("""
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
        row_three_right_layout.addWidget(location_label)
        row_three_right_layout.addWidget(self.location_input)

        row_three_layout.addLayout(row_three_left_layout, 1)
        row_three_layout.addLayout(row_three_right_layout, 1)

        row_four_layout = QHBoxLayout()
        row_four_layout.setSpacing(12)
        row_four_layout.setContentsMargins(0, 0, 0, 0)

        row_four_left_layout = QVBoxLayout()
        row_four_left_layout.setSpacing(4)

        online_platform_type_label = QLabel("Online Platform")
        online_platform_type_label.setStyleSheet("""
                                            color: #334155;
                                            font-size: 13px;
                                        """)

        self.online_platform_type_input = QComboBox()
        self.online_platform_type_input.setMaxVisibleItems(8)
        self.online_platform_type_input.addItem("Zoom", "zoom")
        self.online_platform_type_input.addItem("Microsoft Teams", "microsoft_teams")
        self.online_platform_type_input.addItem("Google Meet", "google meet")
        self.online_platform_type_input.addItem("Slack", "slack")
        self.online_platform_type_input.addItem("Other", "other")

        self.online_platform_type_input.setFixedHeight(36)
        self.online_platform_type_input.setStyleSheet(get_combo_style())

        row_four_left_layout.addWidget(online_platform_type_label)
        row_four_left_layout.addWidget(self.online_platform_type_input)

        row_four_right_layout = QVBoxLayout()
        row_four_right_layout.setSpacing(4)

        appointment_status_label = QLabel("Status")
        appointment_status_label.setStyleSheet("""
                                                    color: #334155;
                                                    font-size: 13px;
                                                """)

        self.appointment_status_input = QComboBox()
        self.appointment_status_input.setMaxVisibleItems(8)
        self.appointment_status_input.addItem("Upcoming", "upcoming")
        self.appointment_status_input.addItem("Completed", "completed")
        self.appointment_status_input.addItem("Missed", "missed")
        self.appointment_status_input.addItem("Canceled", "canceled")
        self.appointment_status_input.addItem("Expired", "expired")

        self.appointment_status_input.setFixedHeight(36)
        self.appointment_status_input.setStyleSheet(get_combo_style())

        row_four_right_layout.addWidget(appointment_status_label)
        row_four_right_layout.addWidget(self.appointment_status_input)

        row_four_layout.addLayout(row_four_left_layout, 1)
        row_four_layout.addLayout(row_four_right_layout, 1)

        notes_row_layout = QVBoxLayout()
        notes_row_layout.setContentsMargins(10, 10, 10, 10)
        notes_row_layout.setSpacing(12)

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

        notes_row_layout.addWidget(notes_label)
        notes_row_layout.addWidget(self.notes_input)

        message_layout = QHBoxLayout()
        message_layout.setContentsMargins(10, 10, 10, 0)

        self.update_appointment_notify_label = QLabel()
        self.update_appointment_notify_label.setWordWrap(True)
        self.update_appointment_notify_label.setStyleSheet("color: #22c55e;font-size: 14px;")

        message_layout.addWidget(self.update_appointment_notify_label)

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

        self.delete_appointment_button = QPushButton("Delete Appointment")
        self.delete_appointment_button.setFixedHeight(40)
        self.delete_appointment_button.setStyleSheet("""
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

        self.delete_appointment_button.clicked.connect(self.delete_appointment_record_clicked)

        self.update_button = QPushButton("Update Appointment")
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

        self.update_button.clicked.connect(self.handle_update_appointment_clicked)

        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.delete_appointment_button)
        button_layout.addWidget(self.update_button)

        edit_appointment_card_layout.addLayout(row_one_layout)
        edit_appointment_card_layout.addLayout(row_two_layout)
        edit_appointment_card_layout.addLayout(row_three_layout)
        edit_appointment_card_layout.addLayout(row_four_layout)
        edit_appointment_card_layout.addLayout(notes_row_layout)
        edit_appointment_card_layout.addLayout(message_layout)
        edit_appointment_card_layout.addWidget(button_row)
        edit_appointment_card_layout.addStretch()

        main_layout.addWidget(self.edit_appointment_card)

    def load_existing_payload(self):

        if self.existing_payload["appointment_type"] == "online":
            self.location_input.setEnabled(False)
        if self.existing_payload["appointment_type"] == "in person":
            self.online_platform_type_input.setEnabled(False)
        self.date_input.setDate(QDate.fromString(self.existing_payload["appointment_date"],"dd/MM/yyyy"))
        self.appointment_time_input.setTime(QTime.fromString(self.existing_payload["appointment_time"],"HH:mm:ss"))
        self.contact_input.setText(self.existing_payload["contact"])
        if self.existing_payload["appointment_location"]:
            self.location_input.setText(self.existing_payload["appointment_location"])
        selected_appointment_type = self.appointment_type_input.findData(self.existing_payload["appointment_type"].lower())
        if selected_appointment_type != -1:
            self.appointment_type_input.setCurrentIndex(selected_appointment_type)
        selected_appointment_status = self.appointment_status_input.findData(self.existing_payload["status"].lower())
        if selected_appointment_status != -1:
            self.appointment_status_input.setCurrentIndex(selected_appointment_status)
        if self.existing_payload["online_platform"]:
            online_platform_index = self.online_platform_type_input.findData(self.existing_payload["online_platform"])
            if online_platform_index != -1:
                self.online_platform_type_input.setCurrentIndex(online_platform_index)
        self.purpose_input.setText(self.existing_payload["appointment_purpose"])
        self.notes_input.setText(self.existing_payload["notes"])

    def handle_update_appointment_clicked(self):

        if not self.validate_update_appointment_form():
            return

        if ((self.date_input.date() > QDate.currentDate() or (self.date_input.date() == QDate.currentDate()
                                                             and self.appointment_time_input.time() > QTime.currentTime()))
                and self.appointment_status_input.currentData() == "completed"):
            reply = QMessageBox.question(
                self,
                "Update Appointment Warning",
                "The appointment time has not been reached yet. \n\n Are you sure you want to mark it as completed?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                self.send_update_appointment_form()
                return



        self.send_update_appointment_form()


    def validate_update_appointment_form(self):

        self.update_appointment_notify_label.setText("")

        if self.contact_input.text().strip() == "":
            self.update_appointment_notify_label.setText(
                "Please enter the person name or organization name you are going to meet")
            return False
        if self.purpose_input.text().strip() == "":
            self.update_appointment_notify_label.setText("Please enter purpose of appointment")
            return False

        if self.appointment_type_input.currentData().strip() == "in person" and self.location_input.text() == "":
            self.update_appointment_notify_label.setText("Please enter location of appointment")
            return False

        if self.date_input.date() == QDate.currentDate() and self.appointment_time_input.time() < QTime.currentTime() and self.appointment_status_input.currentData()=="upcoming":
            self.update_appointment_notify_label.setText("Please enter the valid time of appointment")
            return False

        return True

    def handle_reset_form(self):
        self.update_appointment_notify_label.setText("Form has been reset successfully")
        self.contact_input.clear()
        self.purpose_input.clear()
        self.location_input.clear()
        self.notes_input.setPlainText("")
        QTimer.singleShot(2000, self.clear_notify_label)

    def clear_notify_label(self):
        self.update_appointment_notify_label.setText("")

    def delete_appointment_record_clicked(self):
        reply = QMessageBox.question(
            self,
            "Delete Appointment",
            "Are you sure you want to delete this appointment?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:

            self.handle_delete_appointment_record(self.existing_payload["id"])
            self.contact_input.clear()
            self.purpose_input.clear()
            self.location_input.clear()
            self.notes_input.setPlainText("")
            self.update_appointment_notify_label.setText(
                "Successfully Deleted Appointment"
            )
            QTimer.singleShot(2000, self.reject)

    def send_update_appointment_form(self):
        location = None
        online_platform = None
        if self.appointment_type_input.currentData() == "in person":
            location = self.location_input.text()

        elif self.appointment_type_input.currentData() == "online":
            online_platform = self.online_platform_type_input.currentData()

        updated_appointment_record = {
            "appointment_date": self.date_input.date().toString("yyyy-MM-dd"),
            "appointment_time": self.appointment_time_input.time().toString("hh:mm"),
            "appointment_type": self.appointment_type_input.currentData(),
            "appointment_purpose": self.purpose_input.text(),
            "contact": self.contact_input.text(),
            "appointment_location": location,
            "online_platform": online_platform,
            "status": self.appointment_status_input.currentData(),
            "notes": self.notes_input.toPlainText()
        }

        self.handle_edit_appointment_record(updated_appointment_record, self.existing_payload["id"])
        self.update_appointment_notify_label.setText("Successfully Updated Appointment")
        QTimer.singleShot(2000, self.reject)
