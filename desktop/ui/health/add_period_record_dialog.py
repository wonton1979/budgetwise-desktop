from PySide6.QtCore import QDate, QTime
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QDateEdit, QPushButton, QTextEdit, QCheckBox, \
    QDialog, QFrame

from utils.date_picker_style import get_date_picker_style


class AddPeriodDialog(QDialog):
    def __init__(self,handle_add_health_record):
        super().__init__()
        self.setWindowTitle("Add Period Record")
        self.setModal(True)
        self.resize(600, 320)
        self.initialize_widgets()
        self.handle_add_health_record = handle_add_health_record

    def initialize_widgets(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(4)
        self.setLayout(main_layout)

        self.add_period_record_frame = QFrame()
        self.add_period_record_frame.setStyleSheet("""
                                                       QFrame {
                                                           background-color: white;
                                                           border-radius: 10px;
                                                       }
                                                   """)

        add_period_frame_layout = QVBoxLayout()
        add_period_frame_layout.setContentsMargins(10, 10, 10, 10)
        add_period_frame_layout.setSpacing(4)
        self.add_period_record_frame.setLayout(add_period_frame_layout)

        row_one_layout = QHBoxLayout()
        row_one_layout.setContentsMargins(10,10,10,10)
        row_one_layout.setSpacing(12)

        period_start_date_layout = QVBoxLayout()
        period_start_date_layout.setSpacing(4)

        period_start_date_label = QLabel("Period Start Date")
        period_start_date_label.setStyleSheet("""
                                                  color: #334155;
                                                  font-size: 13px;
                                              """)

        self.period_start_date_input = QDateEdit()
        self.period_start_date_input.setDate(QDate.currentDate())
        self.period_start_date_input.setMaximumDate(QDate.currentDate())
        self.period_start_date_input.setCalendarPopup(True)
        self.period_start_date_input.lineEdit().setReadOnly(True)
        self.period_start_date_input.setFixedHeight(36)
        self.period_start_date_input.setStyleSheet("""
                                                         background-color: #f8fafc;
                                                         border: 1px solid #e2e8f0;
                                                         border-radius: 6px;
                                                         padding: 0 10px;
                                                         font-size: 14px;
                                                     """)
        period_start_date_calendar = self.period_start_date_input.calendarWidget()
        period_start_date_calendar.setMinimumSize(360, 260)
        period_start_date_calendar.setStyleSheet(get_date_picker_style())

        period_start_date_layout.addWidget(period_start_date_label)
        period_start_date_layout.addWidget(self.period_start_date_input)

        period_end_date_layout = QVBoxLayout()
        period_end_date_layout.setSpacing(4)

        self.period_ended_checkbox = QCheckBox("Period Has Ended")
        self.period_ended_checkbox.setFixedHeight(20)
        self.period_ended_checkbox.setStyleSheet("""
                            QCheckBox {
                                font-size: 14px;
                                color: #374151;
                                spacing: 8px;
                            }

                            QCheckBox::indicator {
                                width: 16px;
                                height: 16px;
                            }

                            QCheckBox::indicator:unchecked {
                                border: 2px solid #d1d5db;
                                border-radius: 4px;
                                background-color: white;
                            }

                            QCheckBox::indicator:checked {
                                border: 2px solid #2563eb;
                                border-radius: 4px;
                                background-color: #4f46e5;
                            }
                        """)
        self.period_ended_checkbox.stateChanged.connect(
            self.handle_period_ended_changed
        )

        self.period_end_date_input = QDateEdit()
        self.period_end_date_input.setMinimumDate(QDate(2000, 1, 1))
        self.period_end_date_input.setSpecialValueText("Not Set Yet")
        self.period_end_date_input.setDate(self.period_start_date_input.minimumDate())
        self.period_end_date_input.setMaximumDate(QDate.currentDate())
        self.period_end_date_input.setCalendarPopup(True)
        self.period_end_date_input.lineEdit().setReadOnly(True)
        self.period_end_date_input.setFixedHeight(36)
        self.period_end_date_input.setEnabled(False)
        self.period_end_date_input.setStyleSheet("""
                                                 background-color: #f8fafc;
                                                 border: 1px solid #e2e8f0;
                                                 border-radius: 6px;
                                                 padding: 0 10px;
                                                 font-size: 14px;
                                             """)
        period_end_date_calendar = self.period_end_date_input.calendarWidget()
        period_end_date_calendar.setMinimumSize(360, 260)
        period_end_date_calendar.setStyleSheet(get_date_picker_style())

        period_end_date_layout.addWidget(self.period_ended_checkbox)
        period_end_date_layout.addWidget(self.period_end_date_input)

        row_one_layout.addLayout(period_start_date_layout,1)
        row_one_layout.addLayout(period_end_date_layout,1)

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

        row_two_layout.addWidget(notes_label)
        row_two_layout.addWidget(self.notes_input)

        error_message_layout = QHBoxLayout()
        error_message_layout.setContentsMargins(10, 10, 10, 0)

        self.form_message_label = QLabel("")
        self.form_message_label.setStyleSheet("""
                                                                     color: #ef4444;
                                                                     font-size: 10px;
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

        self.submit_button = QPushButton("Add Period Record")
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

        add_period_frame_layout.addLayout(row_one_layout)
        add_period_frame_layout.addLayout(row_two_layout)
        add_period_frame_layout.addLayout(error_message_layout)
        add_period_frame_layout.addLayout(button_row_layout)

        main_layout.addWidget(self.add_period_record_frame)

    def form_validation(self) -> bool:

        self.form_message_label.setText("")

        if self.period_start_date_input.date() > self.period_end_date_input.date() != QDate(2000, 1, 1):
            self.form_message_label.setText("Period end date cannot be earlier than the start date.")
            return False

        if self.period_start_date_input.date().daysTo(self.period_end_date_input.date()) > 30:
            self.form_message_label.setText("Please check if end date is accurate.")
            return False

        return True

    def handle_form_data_processing(self):

        if not self.form_validation():
            return

        period_end_date = None

        if self.period_end_date_input.date() != QDate(2000, 1, 1):
            period_end_date = self.period_end_date_input.date().toString("yyyy-MM-dd")

        payload = {
            "health_type": "period_record",
            "period_start_date": self.period_start_date_input.date().toString("yyyy-MM-dd"),
            "period_end_date": period_end_date,
            "record_date": QDate.currentDate().toString("yyyy-MM-dd"),
            "record_time": QTime.currentTime().toString("HH:mm"),
            "notes": self.notes_input.toPlainText().strip()
        }
        self.handle_add_health_record(payload)
        self.handle_clear_form()

    def handle_clear_form(self):
        self.notes_input.setText("")


    def handle_period_ended_changed(self):
        if self.period_ended_checkbox.isChecked():
            self.period_end_date_input.setEnabled(True)
            self.period_end_date_input.setDate(QDate.currentDate())
        else:
            self.period_end_date_input.setEnabled(False)
            self.period_end_date_input.setDate(self.period_start_date_input.minimumDate())