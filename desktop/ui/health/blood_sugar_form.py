from PySide6.QtCore import QDate, QTime
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QDateEdit, QPushButton, QComboBox, \
    QTextEdit, QTimeEdit


def get_combo_style():
    return """
           QComboBox {
               background-color: #f8fafc;
               border: 1px solid #e2e8f0;
               border-radius: 6px;
               padding: 0 10px;
               font-size: 14px;
           }

           QComboBox QAbstractItemView {
               background-color: white;
               border: 1px solid #e2e8f0;
               selection-background-color: #e2e8f0;
           }
       """


class BloodSugarForm(QWidget):
    def __init__(self,handle_add_health_record):
        super().__init__()
        self.initialize_widgets()
        self.handle_add_health_record = handle_add_health_record

    def initialize_widgets(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(4)
        self.setLayout(main_layout)

        row_one_layout = QHBoxLayout()
        row_one_layout.setContentsMargins(10,20,10,10)
        row_one_layout.setSpacing(12)

        blood_sugar_reading_layout = QVBoxLayout()
        blood_sugar_reading_layout.setContentsMargins(0,0,0,0)
        blood_sugar_reading_layout.setSpacing(4)


        blood_sugar_reading_label = QLabel("Blood Sugar Reading")
        blood_sugar_reading_label.setStyleSheet("""
            color: #334155;
            font-size: 13px;
        """)

        self.blood_sugar_reading_input = QLineEdit()
        self.blood_sugar_reading_input.setFixedHeight(36)
        self.blood_sugar_reading_input.setStyleSheet("""
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

        blood_sugar_reading_layout.addWidget(blood_sugar_reading_label)
        blood_sugar_reading_layout.addWidget(self.blood_sugar_reading_input)

        blood_sugar_reading_type_layout = QVBoxLayout()
        blood_sugar_reading_type_layout.setContentsMargins(0, 0, 0, 0)
        blood_sugar_reading_type_layout.setSpacing(4)

        blood_sugar_reading_type_label = QLabel("Type Of Reading")
        blood_sugar_reading_type_label.setStyleSheet("""
                    color: #334155;
                    font-size: 13px;
                """)

        self.blood_sugar_reading_type_input = QComboBox()
        self.blood_sugar_reading_type_input.setStyleSheet(get_combo_style())
        self.blood_sugar_reading_type_input.addItem("Fasting", "fasting")
        self.blood_sugar_reading_type_input.addItem("Before Meal", "before_meal")
        self.blood_sugar_reading_type_input.addItem("After Meal", "after_meal")
        self.blood_sugar_reading_type_input.setFixedHeight(36)
        self.blood_sugar_reading_type_input.setMinimumWidth(200)

        blood_sugar_reading_type_layout.addWidget(blood_sugar_reading_type_label)
        blood_sugar_reading_type_layout.addWidget(self.blood_sugar_reading_type_input)

        record_date_layout = QVBoxLayout()
        record_date_layout.setSpacing(4)

        record_date_label = QLabel("Record Date")
        record_date_label.setStyleSheet("""
                                          color: #334155;
                                          font-size: 13px;
                                      """)

        self.record_date_input = QDateEdit()
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
        record_date_calendar.setStyleSheet("""
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

        row_one_layout.addLayout(blood_sugar_reading_layout,1)
        row_one_layout.addLayout(blood_sugar_reading_type_layout,1)
        row_one_layout.addLayout(record_date_layout,1)
        row_one_layout.addLayout(record_time_layout,1)

        row_two_layout = QVBoxLayout()
        row_two_layout.setContentsMargins(10, 10, 10, 10)
        row_two_layout.setSpacing(4)

        notes_label = QLabel("Notes (Optional)")
        notes_label.setStyleSheet("""
                                    color: #334155;
                                    font-size: 13px;
                                """)

        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Add any extra details...")
        self.notes_input.setFixedHeight(50)
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

        row_two_layout.addWidget(notes_label)
        row_two_layout.addWidget(self.notes_input)

        error_message_layout = QHBoxLayout()
        error_message_layout.setContentsMargins(10, 10, 10, 0)

        self.form_error_message_label = QLabel("")
        self.form_error_message_label.setStyleSheet("""
                                                                     color: #ef4444;
                                                                     font-size: 10px;
                                                                 """)

        error_message_layout.addWidget(self.form_error_message_label)

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

        self.submit_button = QPushButton("Add Blood Sugar Record")
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

        main_layout.addLayout(row_one_layout)
        main_layout.addLayout(row_two_layout)
        main_layout.addLayout(error_message_layout)
        main_layout.addLayout(button_row_layout)


    def form_validation(self) -> bool:

        self.form_error_message_label.setText("")

        try:

           blood_sugar_reading = float(self.blood_sugar_reading_input.text())

           if blood_sugar_reading < 3 or blood_sugar_reading > 30:
               self.form_error_message_label.setText("Please enter a realistic blood sugar reading.")
               return False

        except ValueError:
            self.form_error_message_label.setText("Please enter a valid blood sugar reading.")
            return False

        return True

    def handle_form_data_processing(self):

        if not self.form_validation():
            return

        payload ={
            "health_type": "blood_sugar_record",
            "blood_sugar_reading": float(self.blood_sugar_reading_input.text()),
            "blood_sugar_reading_type": self.blood_sugar_reading_type_input.currentData(),
            "record_date": self.record_date_input.date().toString("yyyy-MM-dd"),
            "record_time": self.record_time_input.time().toString("HH:mm"),
            "notes": self.notes_input.toPlainText().strip()
        }
        self.handle_add_health_record(payload)
        self.handle_clear_form()

    def handle_clear_form(self):
        self.blood_sugar_reading_input.setText("")
        self.notes_input.setText("")