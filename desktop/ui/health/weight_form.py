from PySide6.QtCore import QDate, QTime
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QDateEdit, QPushButton, QTextEdit


class WeightForm(QWidget):
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

        weight_value_layout = QVBoxLayout()
        weight_value_layout.setContentsMargins(0,0,0,0)
        weight_value_layout.setSpacing(4)

        weight_value_label_layout = QHBoxLayout()
        weight_value_label_layout.setContentsMargins(0,0,0,0)
        weight_value_label_layout.setSpacing(4)

        weight_value_label = QLabel("Weight Value (Kg)")
        weight_value_label.setStyleSheet("""
            color: #334155;
            font-size: 13px;
        """)

        weight_value_error_label = QLabel("")
        weight_value_error_label.setStyleSheet("""
                                                color: #ef4444;
                                                font-size: 10px;
                                            """)
        weight_value_label_layout.addWidget(weight_value_label)
        weight_value_label_layout.addWidget(weight_value_error_label)

        self.weight_value_input = QLineEdit()
        self.weight_value_input.setFixedHeight(36)
        self.weight_value_input.setStyleSheet("""
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

        weight_value_layout.addLayout(weight_value_label_layout)
        weight_value_layout.addWidget(self.weight_value_input)

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

        row_one_layout.addLayout(weight_value_layout,1)
        row_one_layout.addLayout(record_date_layout,1)

        row_two_layout = QVBoxLayout()
        row_two_layout.setContentsMargins(10, 10, 10, 10)

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

        self.submit_button = QPushButton("Add Weight Record")
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
           weight_value = float(self.weight_value_input.text())
           if weight_value<20 or weight_value>300:
               self.form_error_message_label.setText("Please enter a realistic weight reading.")
               return False
           if len(self.notes_input.toPlainText()) > 255 :
               self.form_error_message_label.setText("Please limit your notes to 255 characters.")
        except ValueError:
            self.form_error_message_label.setText("Please enter a valid blood sugar reading.")
            return False

        return True

    def handle_form_data_processing(self):

        if not self.form_validation():
            return

        payload ={
            "health_type": "weight_record",
            "weight_in_kilograms": float(str(self.weight_value_input.text())),
            "record_date": self.record_date_input.date().toString("yyyy-MM-dd"),
            "record_time": QTime.currentTime().toString("HH:mm"),
            "notes": self.notes_input.toPlainText().strip()
        }
        self.handle_add_health_record(payload)
        self.handle_clear_form()

    def handle_clear_form(self):
        self.weight_value_input.setText("")
        self.notes_input.setText("")






