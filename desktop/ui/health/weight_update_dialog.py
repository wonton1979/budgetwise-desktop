from PySide6.QtCore import QTimer, QDate, QTime
from PySide6.QtWidgets import QDialog, QFrame, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QLineEdit, \
    QTextEdit, QPushButton, QMessageBox, QDateEdit

from utils.date_picker_style import get_date_picker_style


class WeightUpdateDialog(QDialog):
    def __init__(self, handle_edit_weight_record, handle_delete_weight_record, existing_weight_record):
        super().__init__()
        self.health_record_id = None
        self.setWindowTitle("Update Weight Record")
        self.setModal(True)
        self.resize(660, 330)
        self.handle_edit_weight_record = handle_edit_weight_record
        self.handle_delete_weight_record = handle_delete_weight_record
        self.existing_payload = existing_weight_record
        self.create_edit_weight_record_card()
        self.load_existing_payload()

    def create_edit_weight_record_card(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(8, 8, 8, 8)
        self.setLayout(main_layout)

        self.edit_weight_record_card = QFrame()
        self.edit_weight_record_card.setStyleSheet("""
            background-color: white;
            border-radius: 10px;
        """)

        edit_weight_record_card_layout = QVBoxLayout()
        self.edit_weight_record_card.setLayout(edit_weight_record_card_layout)
        edit_weight_record_card_layout.setContentsMargins(20, 20, 20, 20)
        edit_weight_record_card_layout.setSpacing(12)

        row_one_layout = QHBoxLayout()
        row_one_layout.setSpacing(12)
        row_one_layout.setContentsMargins(0, 0, 0, 0)

        row_one_left_layout = QVBoxLayout()
        row_one_left_layout.setSpacing(4)

        weight_reading_label_group_layout = QHBoxLayout()
        weight_reading_label_group_layout.setSpacing(4)
        weight_reading_label_group_layout.setContentsMargins(0, 0, 0, 0)

        weight_reading_label = QLabel("Weight Value (Kg)")
        weight_reading_label.setStyleSheet("""
                                   color: #334155;
                                   font-size: 13px;
                               """)

        self.weight_reading_error = QLabel("")
        self.weight_reading_error.setStyleSheet("""
                                                   color: #ef4444;
                                                   font-size: 12px;
                                               """)

        weight_reading_label_group_layout.addWidget(weight_reading_label)
        weight_reading_label_group_layout.addWidget(self.weight_reading_error)

        self.weight_reading_input = QLineEdit()
        self.weight_reading_input.setFixedHeight(36)
        self.weight_reading_input.setStyleSheet("""
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


        row_one_left_layout.addLayout(weight_reading_label_group_layout)
        row_one_left_layout.addWidget(self.weight_reading_input)

        row_one_right_layout = QVBoxLayout()
        row_one_right_layout.setSpacing(4)

        record_date_label = QLabel("Record Date")
        record_date_label.setStyleSheet("""
                                          color: #334155;
                                          font-size: 13px;
                                      """)

        self.record_date_input = QDateEdit()
        self.record_date_input.setMaximumDate(QDate.currentDate())
        self.record_date_input.setCalendarPopup(True)
        self.record_date_input.lineEdit().setReadOnly(True)
        record_date_calendar = self.record_date_input.calendarWidget()
        record_date_calendar.setMinimumSize(360, 260)
        record_date_calendar.setStyleSheet(get_date_picker_style())

        self.record_date_input.setFixedHeight(36)
        self.record_date_input.setStyleSheet("""
                                                  background-color: #f8fafc;
                                                  border: 1px solid #e2e8f0;
                                                  border-radius: 6px;
                                                  padding: 0 10px;
                                                  font-size: 14px;
                                              """)

        row_one_right_layout.addWidget(record_date_label)
        row_one_right_layout.addWidget(self.record_date_input)

        row_one_layout.addLayout(row_one_left_layout, 1)
        row_one_layout.addLayout(row_one_right_layout, 1)

        edit_weight_record_card_layout.addLayout(row_one_layout)

        row_two_layout = QHBoxLayout()
        row_two_layout.setSpacing(12)
        row_two_layout.setContentsMargins(0, 0, 0, 0)

        #row_two_layout.addLayout(row_two_left_layout, 1)
        #row_two_layout.addLayout(row_two_right_layout, 1)

        edit_weight_record_card_layout.addLayout(row_two_layout)

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

        edit_weight_record_card_layout.addWidget(notes_label)
        edit_weight_record_card_layout.addWidget(self.notes_input)

        self.update_weight_record_notify_label = QLabel()
        self.update_weight_record_notify_label.setWordWrap(True)
        self.update_weight_record_notify_label.setStyleSheet("color: #22c55e;font-size: 14px;")

        edit_weight_record_card_layout.addWidget(self.update_weight_record_notify_label)

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

        self.delete_expense_button = QPushButton("Delete Weight Record")
        self.delete_expense_button.setFixedHeight(40)
        self.delete_expense_button.setStyleSheet("""
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

        self.delete_expense_button.clicked.connect(self.delete_weight_record_clicked)

        self.update_button = QPushButton("Update Weight Record")
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

        self.update_button.clicked.connect(self.handle_update_weight_record_clicked)

        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.delete_expense_button)
        button_layout.addWidget(self.update_button)

        edit_weight_record_card_layout.addWidget(button_row)
        edit_weight_record_card_layout.addStretch()

        main_layout.addWidget(self.edit_weight_record_card)

    def load_existing_payload(self):

        self.health_record_id = self.existing_payload["health_record_id"]
        self.weight_reading_input.setText(str(self.existing_payload["weight_in_kilograms"]))
        self.record_date_input.setDate(QDate.fromString(self.existing_payload["record_date"],"dd/MM/yyyy"))
        self.notes_input.setText(self.existing_payload["notes"])


    def handle_update_weight_record_clicked(self):

        if not self.validate_update_weight_record_form():
            return

        updated_weight_record = {
            "health_type": "weight_record",
            "weight_in_kilograms": self.weight_reading_input.text().strip(),
            "record_date": self.record_date_input.date().toString("yyyy-MM-dd"),
            "record_time": QTime.currentTime().toString("hh:mm"),
            "notes": self.notes_input.toPlainText().strip() or None,
        }

        self.handle_edit_weight_record(self.health_record_id, updated_weight_record)
        self.update_weight_record_notify_label.setText("Successfully Updated Weight Record")
        QTimer.singleShot(2000, self.reject)

    def validate_update_weight_record_form(self):

        self.weight_reading_error.setText("")

        try:
           weight_value = float(self.weight_reading_input.text())
           if weight_value<20 or weight_value>300:
               self.weight_reading_error.setText("Please enter a realistic weight reading.")
               return False
           if len(self.notes_input.toPlainText()) > 255 :
               self.weight_reading_error.setText("Please limit your notes to 255 characters.")
        except ValueError:
            self.weight_reading_error.setText("Please enter a valid weight reading.")
            return False

        return True

    def handle_reset_form(self):
        self.update_weight_record_notify_label.setText("Form has been reset successfully")
        self.weight_reading_input.setText("")
        self.notes_input.setPlainText("")
        QTimer.singleShot(2000, self.clear_notify_label)

    def clear_notify_label(self):
        self.update_weight_record_notify_label.setText("")

    def delete_weight_record_clicked(self):
        reply = QMessageBox.question(
            self,
            "Delete Record",
            "Are you sure you want to delete this record?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:

            self.handle_delete_weight_record(self.health_record_id)
            self.weight_reading_input.setText("")
            self.notes_input.setPlainText("")
            self.update_weight_record_notify_label.setText(
                "Successfully Deleted Weight Record"
            )
            QTimer.singleShot(2000, self.reject)
