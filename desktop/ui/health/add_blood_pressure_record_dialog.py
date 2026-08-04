from PySide6.QtCore import QDate, QTime
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QDateEdit, QPushButton, QTextEdit, \
    QTimeEdit, QDialog, QFrame

from ui.components.popup_date_edit import PopupDateEdit
from utils.date_picker_style import get_date_picker_style


class AddBloodPressureRecord(QDialog):
    def __init__(self,handle_add_health_record,date_format):
        super().__init__()
        self.setWindowTitle("Add Blood Pressure Record")
        self.setModal(True)
        self.resize(600, 380)
        self.date_format = date_format
        self.initialize_widgets()
        self.handle_add_health_record = handle_add_health_record

    def initialize_widgets(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(4)
        self.setLayout(main_layout)

        self.add_blood_pressure_record_frame = QFrame()
        self.add_blood_pressure_record_frame.setStyleSheet("""
                                       QFrame {
                                           background-color: white;
                                           border-radius: 10px;
                                       }
                                   """)

        add_blood_pressure_record_frame_layout = QVBoxLayout()
        add_blood_pressure_record_frame_layout.setContentsMargins(10, 10, 10, 10)
        add_blood_pressure_record_frame_layout.setSpacing(4)
        self.add_blood_pressure_record_frame.setLayout(add_blood_pressure_record_frame_layout)

        row_one_layout = QHBoxLayout()
        row_one_layout.setContentsMargins(10,10,10,10)
        row_one_layout.setSpacing(12)

        systolic_reading_layout = QVBoxLayout()
        systolic_reading_layout.setContentsMargins(0,0,0,0)
        systolic_reading_layout.setSpacing(4)


        systolic_reading_label = QLabel("Systolic Reading")
        systolic_reading_label.setStyleSheet("""
            color: #334155;
            font-size: 13px;
        """)

        self.systolic_reading_input = QLineEdit()
        self.systolic_reading_input.setFixedHeight(36)
        self.systolic_reading_input.setStyleSheet("""
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

        systolic_reading_layout.addWidget(systolic_reading_label)
        systolic_reading_layout.addWidget(self.systolic_reading_input)

        diastolic_reading_layout = QVBoxLayout()
        diastolic_reading_layout.setContentsMargins(0, 0, 0, 0)
        diastolic_reading_layout.setSpacing(4)

        diastolic_reading_label = QLabel("Diastolic Reading")
        diastolic_reading_label.setStyleSheet("""
                    color: #334155;
                    font-size: 13px;
                """)

        self.diastolic_reading_input = QLineEdit()
        self.diastolic_reading_input.setFixedHeight(36)
        self.diastolic_reading_input.setStyleSheet("""
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

        diastolic_reading_layout.addWidget(diastolic_reading_label)
        diastolic_reading_layout.addWidget(self.diastolic_reading_input)

        heart_rate_reading_layout = QVBoxLayout()
        heart_rate_reading_layout.setContentsMargins(0, 0, 0, 0)
        heart_rate_reading_layout.setSpacing(4)

        heart_rate_reading_label = QLabel("Heart Rate Reading")
        heart_rate_reading_label.setStyleSheet("""
                    color: #334155;
                    font-size: 13px;
                """)

        self.heart_rate_reading_input = QLineEdit()
        self.heart_rate_reading_input.setFixedHeight(36)
        self.heart_rate_reading_input.setStyleSheet("""
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

        heart_rate_reading_layout.addWidget(heart_rate_reading_label)
        heart_rate_reading_layout.addWidget(self.heart_rate_reading_input)


        row_one_layout.addLayout(systolic_reading_layout,1)
        row_one_layout.addLayout(diastolic_reading_layout,1)
        row_one_layout.addLayout(heart_rate_reading_layout,1)

        row_two_layout = QHBoxLayout()
        row_two_layout.setContentsMargins(10, 10, 10, 10)
        row_two_layout.setSpacing(12)

        record_date_layout = QVBoxLayout()
        record_date_layout.setSpacing(4)

        record_date_label = QLabel("Record Date")
        record_date_label.setStyleSheet("""
                                                  color: #334155;
                                                  font-size: 13px;
                                              """)

        self.record_date_input = PopupDateEdit()
        self.record_date_input.setDate(QDate.currentDate())
        self.record_date_input.setMaximumDate(QDate.currentDate())
        self.record_date_input.setCalendarPopup(True)
        self.record_date_input.lineEdit().setReadOnly(True)
        self.record_date_input.setFixedHeight(36)
        self.record_date_input.setStyleSheet("""
                                                         background-color: #f8fafc;
                                                         border: 1px solid #e2e8f0;
                                                         border-radius: 6px;
                                                         padding: 0 10px;
                                                         font-size: 14px;
                                                     """)
        record_date_calendar = self.record_date_input.calendarWidget()
        record_date_calendar.setMinimumSize(360, 260)
        record_date_calendar.setStyleSheet(get_date_picker_style())

        record_date_layout.addWidget(record_date_label)
        record_date_layout.addWidget(self.record_date_input)

        record_time_layout = QVBoxLayout()
        record_time_layout.setSpacing(4)

        record_time_label = QLabel("Record Time")
        record_time_label.setStyleSheet("""
                                                          color: #334155;
                                                          font-size: 13px;
                                                      """)

        self.record_time_input = QTimeEdit()
        self.record_time_input.setDisplayFormat("HH:mm")
        self.record_time_input.setTime(QTime.currentTime())
        self.record_time_input.setStyleSheet("""
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
        self.record_time_input.setFixedHeight(36)

        record_time_layout.addWidget(record_time_label)
        record_time_layout.addWidget(self.record_time_input)


        row_two_layout.addLayout(record_date_layout, 1)
        row_two_layout.addLayout(record_time_layout, 1)

        notes_layout = QVBoxLayout()
        notes_layout .setContentsMargins(10, 10, 10, 10)
        notes_layout .setSpacing(4)

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

        notes_layout.addWidget(notes_label)
        notes_layout.addWidget(self.notes_input)

        error_message_layout = QHBoxLayout()
        error_message_layout.setContentsMargins(10, 10, 10, 0)

        self.form_message_label = QLabel("")
        self.form_message_label.setStyleSheet("""
                                                                     color: #ef4444;
                                                                     font-size: 14px;
                                                                 """)

        error_message_layout.addWidget(self.form_message_label)

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

        self.submit_button = QPushButton("Add Blood Pressure Record")
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

        self.submit_button.clicked.connect(self.handle_form_data_processing)

        button_row_layout.addWidget(self.clear_button)
        button_row_layout.addWidget(self.submit_button)

        add_blood_pressure_record_frame_layout.addLayout(row_one_layout)
        add_blood_pressure_record_frame_layout.addLayout(row_two_layout)
        add_blood_pressure_record_frame_layout.addLayout(notes_layout)
        add_blood_pressure_record_frame_layout.addLayout(error_message_layout)
        add_blood_pressure_record_frame_layout.addLayout(button_row_layout)

        main_layout.addWidget(self.add_blood_pressure_record_frame)

    def form_validation(self) -> bool:

        self.form_message_label.setText("")

        try:
           systolic_reading = int(self.systolic_reading_input.text())
           diastolic_reading = int(self.diastolic_reading_input.text())
           heart_rate_reading = int(self.heart_rate_reading_input.text())

           if systolic_reading < 100 or systolic_reading > 300:
               self.form_message_label.setText("Please enter a realistic systolic reading.")
               return False

           if diastolic_reading < 20 or diastolic_reading > 150:
               self.form_message_label.setText("Please enter a realistic diastolic reading.")
               return False

           if heart_rate_reading < 20 or heart_rate_reading > 200:
               self.form_message_label.setText("Please enter a realistic heart rate reading.")
               return False

           if diastolic_reading > systolic_reading :
               self.form_message_label.setText("Diastolic reading can not be greater than systolic reading.")
               return False


        except ValueError:
            self.form_message_label.setText("Please enter a valid reading.")
            return False

        return True

    def handle_form_data_processing(self):

        if not self.form_validation():
            return

        payload ={
            "health_type": "blood_pressure_record",
            "systolic_reading": int(self.systolic_reading_input.text()),
            "diastolic_reading":int(self.diastolic_reading_input.text()),
            "heart_rate": int(self.heart_rate_reading_input.text()),
            "record_date": self.record_date_input.date().toString("yyyy-MM-dd"),
            "record_time": self.record_time_input.time().toString("HH:mm"),
            "notes": self.notes_input.toPlainText().strip()
        }

        self.handle_add_health_record(payload)
        self.handle_clear_form()

    def handle_clear_form(self):
        self.systolic_reading_input.setText("")
        self.diastolic_reading_input.setText("")
        self.heart_rate_reading_input.setText("")
        self.notes_input.setText("")

    def set_current_date_format(self,current_date_format = None):
        if current_date_format:
            self.date_format = current_date_format
        match self.date_format:
            case "YYYY-MM-DD":
                self.record_date_input.setDisplayFormat("yyyy-MM-dd")
            case "DD MMM YYYY":
                self.record_date_input.setDisplayFormat("dd MMM yyyy")
            case "DD/MM/YYYY":
                self.record_date_input.setDisplayFormat("dd/MM/yyyy")