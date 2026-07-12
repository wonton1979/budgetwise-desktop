from PySide6.QtCore import QTimer, QDate, QTime
from PySide6.QtWidgets import QDialog, QFrame, QVBoxLayout, QWidget, QHBoxLayout, QLabel, \
    QTextEdit, QPushButton, QMessageBox, QDateEdit

from utils.date_picker_style import get_date_picker_style


class PeriodUpdateDialog(QDialog):
    def __init__(self, handle_edit_health_record, handle_delete_health_record, existing_period_record,date_format):
        super().__init__()
        self.health_record_id = None
        self.date_loading_format = None
        self.setWindowTitle("Update Period Record")
        self.setModal(True)
        self.resize(660, 330)
        self.handle_edit_health_record = handle_edit_health_record
        self.handle_delete_health_record = handle_delete_health_record
        self.existing_payload = existing_period_record
        self.date_format = date_format
        self.create_edit_period_record_card()
        self.load_existing_payload()

    def create_edit_period_record_card(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(8, 8, 8, 8)
        self.setLayout(main_layout)

        self.edit_health_record_card = QFrame()
        self.edit_health_record_card.setStyleSheet("""
            background-color: white;
            border-radius: 10px;
        """)

        edit_period_record_card_layout = QVBoxLayout()
        self.edit_health_record_card.setLayout(edit_period_record_card_layout)
        edit_period_record_card_layout.setContentsMargins(20, 20, 20, 20)
        edit_period_record_card_layout.setSpacing(12)

        row_one_layout = QHBoxLayout()
        row_one_layout.setSpacing(12)
        row_one_layout.setContentsMargins(0, 0, 0, 0)

        period_start_date_layout = QVBoxLayout()
        period_start_date_layout.setSpacing(4)

        period_start_date_label = QLabel("Period Start Date")
        period_start_date_label.setStyleSheet("""
                                                          color: #334155;
                                                          font-size: 13px;
                                                      """)

        self.period_start_date_input = QDateEdit()
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
        self.period_start_date_input.dateChanged.connect(self.handle_start_date_changed)

        period_start_date_layout.addWidget(period_start_date_label)
        period_start_date_layout.addWidget(self.period_start_date_input)

        period_end_date_layout = QVBoxLayout()
        period_end_date_layout.setSpacing(4)

        period_end_date_label = QLabel("Period End Date")
        period_end_date_label.setStyleSheet("""
                                          color: #334155;
                                          font-size: 13px;
                                      """)

        self.period_end_date_input = QDateEdit()
        self.period_end_date_input.setMaximumDate(QDate.currentDate())
        self.period_end_date_input.setCalendarPopup(True)
        self.period_end_date_input.lineEdit().setReadOnly(True)
        period_end_date_calendar = self.period_end_date_input.calendarWidget()
        period_end_date_calendar.setMinimumSize(360, 260)
        period_end_date_calendar.setStyleSheet(get_date_picker_style())

        self.period_end_date_input.setFixedHeight(36)
        self.period_end_date_input.setStyleSheet("""
                                                  background-color: #f8fafc;
                                                  border: 1px solid #e2e8f0;
                                                  border-radius: 6px;
                                                  padding: 0 10px;
                                                  font-size: 14px;
                                              """)

        period_end_date_layout.addWidget(period_end_date_label)
        period_end_date_layout.addWidget(self.period_end_date_input)

        row_one_layout.addLayout(period_start_date_layout, 1)
        row_one_layout.addLayout(period_end_date_layout, 1)

        edit_period_record_card_layout.addLayout(row_one_layout)

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

        edit_period_record_card_layout.addWidget(notes_label)
        edit_period_record_card_layout.addWidget(self.notes_input)

        self.update_period_record_notify_label = QLabel()
        self.update_period_record_notify_label.setWordWrap(True)
        self.update_period_record_notify_label.setStyleSheet("color: #22c55e;font-size: 14px;")

        edit_period_record_card_layout.addWidget(self.update_period_record_notify_label)

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

        self.delete_period_record_button = QPushButton("Delete Period Record")
        self.delete_period_record_button.setFixedHeight(40)
        self.delete_period_record_button.setStyleSheet("""
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

        self.delete_period_record_button.clicked.connect(self.delete_period_record_clicked)

        self.update_button = QPushButton("Update Period Record")
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

        self.update_button.clicked.connect(self.handle_update_period_record_clicked)

        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.delete_period_record_button)
        button_layout.addWidget(self.update_button)

        edit_period_record_card_layout.addWidget(button_row)
        edit_period_record_card_layout.addStretch()

        self.set_current_date_format()

        main_layout.addWidget(self.edit_health_record_card)

    def load_existing_payload(self):
        self.health_record_id = int(self.existing_payload["health_record_id"])
        self.period_start_date_input.setDate(QDate.fromString(self.existing_payload["start_date"],self.date_loading_format))
        if self.existing_payload["end_date"]:
            self.period_end_date_input.setDate(QDate.fromString(self.existing_payload["end_date"],self.date_loading_format))
        else:
            self.period_end_date_input.setMinimumDate(QDate.fromString(self.existing_payload["start_date"],self.date_loading_format).addDays(-1))
            self.period_end_date_input.setSpecialValueText("Not Set Yet")

        self.notes_input.setText(self.existing_payload["notes"])


    def handle_update_period_record_clicked(self):

        if not self.validate_update_period_record_form():
            return

        period_end_date = None

        if self.period_end_date_input.date() != self.period_start_date_input.date().addDays(-1):
            period_end_date = self.period_end_date_input.date().toString("yyyy-MM-dd")

        updated_period_record = {
            "health_type": "period_record",
            "period_start_date": self.period_start_date_input.date().toString("yyyy-MM-dd"),
            "period_end_date": period_end_date,
            "record_date": QDate.currentDate().toString("yyyy-MM-dd"),
            "record_time": QTime.currentTime().toString("HH:mm"),
            "notes": self.notes_input.toPlainText().strip()
        }

        self.handle_edit_health_record(self.health_record_id, updated_period_record)
        self.update_period_record_notify_label.setText("Successfully Updated Weight Record")
        QTimer.singleShot(2000, self.accept)

    def validate_update_period_record_form(self):

        self.update_period_record_notify_label.setText("")

        if self.period_start_date_input.date() > self.period_end_date_input.date():
            self.update_period_record_notify_label.setText("Period end date cannot be earlier than the start date.")
            return False

        if self.period_start_date_input.date().daysTo(self.period_end_date_input.date()) > 30 and self.period_end_date_input.specialValueText() != "Not Set Yet":
            self.update_period_record_notify_label.setText("Periods longer than 30 days are uncommon. \n\nPlease check your dates or consult a healthcare professional if this is accurate.")
            return False

        return True

    def handle_reset_form(self):
        self.update_period_record_notify_label.setText("Form has been reset successfully")
        self.notes_input.setPlainText("")
        QTimer.singleShot(2000, self.clear_notify_label)

    def clear_notify_label(self):
        self.update_period_record_notify_label.setText("")

    def delete_period_record_clicked(self):
        reply = QMessageBox.question(
            self,
            "Delete Record",
            "Are you sure you want to delete this record?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:

            self.handle_delete_health_record(self.health_record_id)
            self.notes_input.setPlainText("")
            self.update_period_record_notify_label.setText(
                "Successfully Deleted Period Record"
            )
            QTimer.singleShot(2000, self.accept)

    def handle_start_date_changed(self):
        self.period_end_date_input.setMinimumDate(self.period_start_date_input.date().addDays(-1))


    def set_current_date_format(self):

        match self.date_format:
            case "YYYY-MM-DD":
                self.period_start_date_input.setDisplayFormat("yyyy-MM-dd")
                self.period_end_date_input.setDisplayFormat("yyyy-MM-dd")
                self.date_loading_format ="yyyy-MM-dd"
            case "DD MMM YYYY":
                self.period_start_date_input.setDisplayFormat("dd MMM yyyy")
                self.period_end_date_input.setDisplayFormat("dd MMM yyyy")
                self.date_loading_format ="dd MMM yyyy"
            case "DD/MM/YYYY":
                self.period_start_date_input.setDisplayFormat("dd/MM/yyyy")
                self.period_end_date_input.setDisplayFormat("dd/MM/yyyy")
                self.date_loading_format ="dd/MM/yyyy"