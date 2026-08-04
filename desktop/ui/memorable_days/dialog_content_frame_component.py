from PySide6.QtCore import QDate, QTimer
from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QDateEdit, QTextEdit, \
    QPushButton, QMessageBox

from ui.components.popup_date_edit import PopupDateEdit
from utils.combobox_style import get_combo_style
from utils.date_picker_style import get_date_picker_style


class ContentFrameComponent(QFrame):
    def __init__(self,handle_add_memorable_day = None,
                 handle_update_memory_day = None,
                 handle_delete_memory_day = None,
                 existing_memorable_day_data = None,
                 operation = None,
                 date_format = None,
                 ):
        super().__init__()
        self.handle_add_memorable_day = handle_add_memorable_day
        self.handle_update_memory_day = handle_update_memory_day
        self.handle_delete_memory_day = handle_delete_memory_day
        self.existing_memorable_day_data = existing_memorable_day_data
        self.operation = operation
        self.date_format = date_format
        self.date_loading_format = None
        self.ui_setup()
        if self.operation == "update":
            self.load_existing_memorable_day_data()


    def ui_setup(self):
        self.setStyleSheet("""
                    background-color: white;
                    border-radius: 10px;
                """)

        add_memorable_day_card_layout = QVBoxLayout()
        self.setLayout(add_memorable_day_card_layout)
        add_memorable_day_card_layout.setContentsMargins(20, 20, 20, 20)
        add_memorable_day_card_layout.setSpacing(12)

        row_one_layout = QHBoxLayout()
        row_one_layout.setSpacing(12)
        row_one_layout.setContentsMargins(0, 0, 0, 0)

        row_one_left_layout = QVBoxLayout()
        row_one_left_layout.setSpacing(4)

        event_name_label = QLabel("Event Name")
        event_name_label.setStyleSheet("""
                                           color: #334155;
                                           font-size: 13px;
                                       """)

        self.event_name_input = QLineEdit()
        self.event_name_input.setFixedHeight(36)
        self.event_name_input.setStyleSheet("""
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

        row_one_left_layout.addWidget(event_name_label)
        row_one_left_layout.addWidget(self.event_name_input)

        row_one_middle_layout = QVBoxLayout()
        row_one_middle_layout.setSpacing(4)

        memorable_day_type_label = QLabel("Memorable Day Type")
        memorable_day_type_label.setStyleSheet("""
                                           color: #334155;
                                           font-size: 13px;
                                       """)

        self.memorable_day_type_input = QComboBox()
        self.memorable_day_type_input.setStyleSheet(get_combo_style())
        self.memorable_day_type_input.addItem("Birthday", "birthday")
        self.memorable_day_type_input.addItem("Anniversary", "anniversary")
        self.memorable_day_type_input.addItem("Other", "other")
        self.memorable_day_type_input.setFixedHeight(36)

        row_one_middle_layout.addWidget(memorable_day_type_label)
        row_one_middle_layout.addWidget(self.memorable_day_type_input)

        row_one_right_layout = QVBoxLayout()
        row_one_right_layout.setSpacing(4)

        event_date_label = QLabel("Event Date")
        event_date_label.setStyleSheet("""
                                                 color: #334155;
                                                 font-size: 13px;
                                             """)

        self.event_date_input = PopupDateEdit()

        self.event_date_input.setCalendarPopup(True)
        self.event_date_input.lineEdit().setReadOnly(True)
        self.event_date_input.setDate(QDate.currentDate())
        self.set_current_date_format()

        event_date_calendar = self.event_date_input.calendarWidget()
        event_date_calendar.setMinimumSize(360, 260)
        event_date_calendar.setStyleSheet(get_date_picker_style())

        self.event_date_input.setFixedHeight(36)
        self.event_date_input.setStyleSheet("""
                                                         background-color: #f8fafc;
                                                         border: 1px solid #e2e8f0;
                                                         border-radius: 6px;
                                                         padding: 0 10px;
                                                         font-size: 14px;
                                                     """)

        row_one_right_layout.addWidget(event_date_label)
        row_one_right_layout.addWidget(self.event_date_input)

        row_one_layout.addLayout(row_one_left_layout, 1)
        row_one_layout.addLayout(row_one_middle_layout, 1)
        row_one_layout.addLayout(row_one_right_layout, 1)

        add_memorable_day_card_layout.addLayout(row_one_layout)

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

        add_memorable_day_card_layout.addWidget(notes_label)
        add_memorable_day_card_layout.addWidget(self.notes_input)

        self.memorable_day_notify_label = QLabel()
        self.memorable_day_notify_label.setWordWrap(True)
        self.memorable_day_notify_label.setStyleSheet("color: #22c55e;font-size: 14px;")

        add_memorable_day_card_layout.addWidget(self.memorable_day_notify_label)

        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 20, 0, 0)
        button_layout.setSpacing(12)

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

        if self.operation == "add":
            self.add_button = QPushButton("Add Memorable Day")
            self.add_button.setFixedHeight(40)
            self.add_button.setStyleSheet("""
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

            self.add_button.clicked.connect(self.handle_add_memorable_day_button_clicked)

            button_layout.addWidget(self.clear_button)
            button_layout.addWidget(self.add_button)
            self.event_date_input.setDisplayFormat(self.date_loading_format)
            add_memorable_day_card_layout.addLayout(button_layout)
            add_memorable_day_card_layout.addStretch()

        if self.operation == "update":
            self.delete_button = QPushButton("Delete Memorable Day")
            self.delete_button.setFixedHeight(40)
            self.delete_button.setStyleSheet("""
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

            self.delete_button.clicked.connect(self.handle_delete_memorable_day_button_clicked)

            self.update_button = QPushButton("Update Memorable Day")
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

            self.update_button.clicked.connect(self.handle_update_memorable_day_button_clicked)

            button_layout.addWidget(self.clear_button)
            button_layout.addWidget(self.delete_button)
            button_layout.addWidget(self.update_button)

            self.event_date_input.setDisplayFormat(self.date_loading_format)
            add_memorable_day_card_layout.addLayout(button_layout)
            add_memorable_day_card_layout.addStretch()

    def load_existing_memorable_day_data(self):
        self.event_name_input.setText(self.existing_memorable_day_data["event_name"])
        memorable_day_index = self.memorable_day_type_input.findData(self.existing_memorable_day_data["memorable_day_type"])
        if memorable_day_index != -1:
            self.memorable_day_type_input.setCurrentIndex(memorable_day_index)
        self.event_date_input.setDate(QDate.fromString(self.existing_memorable_day_data["memorable_date"],self.date_loading_format))

        self.notes_input.setPlainText(self.existing_memorable_day_data["notes"])

    def validate_add_memorable_day_form(self):

        self.memorable_day_notify_label.setText("")

        event_name_text = self.event_name_input.text().strip()

        if not event_name_text:
            self.memorable_day_notify_label.setText("Event Name Is Required")
            return False

        return True

    def handle_reset_form(self):
        self.memorable_day_notify_label.setText("Form has been reset successfully")
        self.event_name_input.setText("")
        self.notes_input.setPlainText("")
        QTimer.singleShot(2000, self.clear_notify_label)

    def clear_notify_label(self):
        self.memorable_day_notify_label.setText("")

    def handle_add_memorable_day_button_clicked(self):

        if not self.validate_add_memorable_day_form():
            return

        self.handle_add_memorable_day(self.get_current_form_data())

        self.memorable_day_notify_label.setText("Successfully added memorable day")

        self.handle_reset_form()

    def handle_update_memorable_day_button_clicked(self):

        if not self.validate_add_memorable_day_form():
            return

        self.handle_update_memory_day(self.get_current_form_data(),self.existing_memorable_day_data["id"])

        self.memorable_day_notify_label.setText("Successfully updated memorable day")

        self.handle_reset_form()

    def handle_delete_memorable_day_button_clicked(self):
        reply = QMessageBox.question(
            self,
            "Delete Memorable Day",
            "Are you sure you want to delete this memorable day?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.handle_delete_memory_day(self.existing_memorable_day_data["id"])
            self.handle_reset_form()
            self.memorable_day_notify_label.setText(
                "Successfully Deleted Appointment"
            )


    def get_current_form_data(self):

        new_memorable_day_data = {
            "event_name": self.event_name_input.text().strip(),
            "memorable_date": self.event_date_input.date().toString("yyyy-MM-dd"),
            "memorable_day_type": self.memorable_day_type_input.currentData(),
            "notes": self.notes_input.toPlainText().strip() or None,
        }

        return new_memorable_day_data

    def set_current_date_format(self):

        match self.date_format:
            case "YYYY-MM-DD":
                self.date_loading_format = "yyyy-MM-dd"
            case "DD MMM YYYY":
                self.date_loading_format = "dd MMM yyyy"
            case "DD/MM/YYYY":
                self.date_loading_format = "dd/MM/yyyy"

