from PySide6.QtCore import QDate, QTime
from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QDateEdit, QTimeEdit, QComboBox, QLineEdit, \
    QPushButton, QTextEdit, QDialog

from utils.combobox_style import get_combo_style
from utils.date_picker_style import get_date_picker_style


class AddAppointmentsDialog(QDialog):

    def __init__(self,handle_create_appointment):
        super().__init__()
        self.setWindowTitle("Add Appointment")
        self.setModal(True)
        self.resize(600, 390)
        self.handle_create_appointment = handle_create_appointment
        self.add_appointment_ui()


    def add_appointment_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)

        self.add_appointment_frame = QFrame()
        self.add_appointment_frame.setStyleSheet("""
                                                               QFrame {
                                                                   background-color: white;
                                                                   border-radius: 10px;
                                                               }
                                                           """)

        add_appointment_layout = QVBoxLayout()
        add_appointment_layout.setContentsMargins(10, 10, 10, 10)
        add_appointment_layout.setSpacing(4)
        self.add_appointment_frame.setLayout(add_appointment_layout)


        row_one_layout = QHBoxLayout()
        row_one_layout.setContentsMargins(10, 10, 10,10)
        row_one_layout.setSpacing(4)

        row_one_left_layout = QVBoxLayout()
        row_one_left_layout.setContentsMargins(0, 0, 0, 0)
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
        row_one_right_layout.setContentsMargins(0, 0, 0, 0)
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
        row_one_layout.addLayout(row_one_right_layout, 1)

        row_two_layout = QHBoxLayout()
        row_two_layout.setContentsMargins(10, 10, 10, 10)
        row_two_layout.setSpacing(4)

        row_two_left_layout = QVBoxLayout()
        row_two_left_layout.setContentsMargins(0, 0, 0, 0)
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
        row_two_right_layout.setContentsMargins(0, 0, 0, 0)
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


        row_two_layout.addLayout(row_two_left_layout,1)
        row_two_layout.addLayout(row_two_right_layout,1)

        row_three_layout = QHBoxLayout()
        row_three_layout.setContentsMargins(10, 10, 10, 10)
        row_three_layout.setSpacing(4)

        row_three_left_layout = QVBoxLayout()
        row_three_left_layout.setContentsMargins(0, 0, 0, 0)
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
        self.appointment_type_input.currentTextChanged.connect(self.appointment_type_changed)

        row_three_left_layout.addWidget(appointment_type_label)
        row_three_left_layout.addWidget(self.appointment_type_input)

        row_three_middle_layout = QVBoxLayout()
        row_three_middle_layout.setContentsMargins(0, 0, 0, 0)
        row_three_middle_layout.setSpacing(4)

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

        row_three_middle_layout.addWidget(location_label)
        row_three_middle_layout.addWidget(self.location_input)

        row_three_right_layout = QVBoxLayout()
        row_three_right_layout.setContentsMargins(0, 0, 0, 0)
        row_three_right_layout.setSpacing(4)

        online_platform_type_label = QLabel("Online Platform")
        online_platform_type_label .setStyleSheet("""
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
        self.online_platform_type_input.setEnabled(False)


        row_three_right_layout.addWidget(online_platform_type_label)
        row_three_right_layout.addWidget(self.online_platform_type_input)

        row_three_layout.addLayout(row_three_left_layout,1)
        row_three_layout.addLayout(row_three_middle_layout,1)
        row_three_layout.addLayout(row_three_right_layout,1)

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

        self.form_message_label = QLabel("")
        self.form_message_label.setStyleSheet("""
                                                                             color: #ef4444;
                                                                             font-size: 14px;
                                                                         """)

        message_layout.addWidget(self.form_message_label)

        button_row_layout = QHBoxLayout()
        button_row_layout.setContentsMargins(10, 10, 10, 10)
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

        self.submit_button = QPushButton("Add Appointment")
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

        self.submit_button.clicked.connect(self.handle_add_appointment_button_clicked)

        button_row_layout.addWidget(self.clear_button)
        button_row_layout.addWidget(self.submit_button)

        add_appointment_layout.addLayout(row_one_layout)
        add_appointment_layout.addLayout(row_two_layout)
        add_appointment_layout.addLayout(row_three_layout)
        add_appointment_layout.addLayout(notes_row_layout)
        add_appointment_layout.addLayout(message_layout)
        add_appointment_layout.addLayout(button_row_layout)

        main_layout.addWidget(self.add_appointment_frame)

    def handle_clear_form(self):
        self.purpose_input.clear()
        self.contact_input.clear()
        self.notes_input.clear()
        self.location_input.clear()

    def handle_add_appointment_button_clicked(self):

        if not self.form_validation():
            return

        location = None
        online_platform = None
        if self.appointment_type_input.currentData() == "in person":
            location = self.location_input.text()
        elif self.appointment_type_input.currentData() == "online":
            online_platform = self.online_platform_type_input.currentData()
        payload= {
            "appointment_date": self.date_input.date().toString("yyyy-MM-dd"),
            "appointment_time": self.appointment_time_input.time().toString("hh:mm"),
            "appointment_type": self.appointment_type_input.currentData(),
            "appointment_purpose": self.purpose_input.text(),
            "contact": self.contact_input.text(),
            "appointment_location": location,
            "online_platform": online_platform,
            "notes": self.notes_input.toPlainText()
        }
        self.handle_create_appointment(payload)
        self.handle_clear_form()

    def form_validation(self):

        self.form_message_label.setText("")

        if self.contact_input.text().strip() == "":
            self.form_message_label.setText("Please enter the person name or organization name you are going to meet")
            return False
        if self.purpose_input.text().strip() == "":
            self.form_message_label.setText("Please enter purpose of appointment")
            return False

        if self.appointment_type_input.currentData().strip() == "in person" and self.location_input.text() == "":
            self.form_message_label.setText("Please enter location of appointment")
            return False

        if self.date_input.date() == QDate.currentDate() and self.appointment_time_input.time() < QTime.currentTime():
            self.form_message_label.setText("Please enter the valid time of appointment")
            return False

        return True

    def appointment_type_changed(self):
        if self.appointment_type_input.currentData() == "online":
            self.online_platform_type_input.setEnabled(True)
            self.location_input.setEnabled(False)
        else:
            self.online_platform_type_input.setEnabled(False)
            self.location_input.setEnabled(True)

