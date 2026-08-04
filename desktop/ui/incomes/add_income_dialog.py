from PySide6.QtCore import QDate
from PySide6.QtWidgets import QDialog, QFrame, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QLineEdit, QTextEdit, \
    QPushButton, QDateEdit

from ui.components.popup_date_edit import PopupDateEdit
from utils.combobox_style import get_combo_style
from utils.date_picker_style import get_date_picker_style


class AddIncomeDialog(QDialog):
    def __init__(self,handle_add_income,date_format):
        super().__init__()
        self.income_id = None
        self.setWindowTitle("Add Income")
        self.setModal(True)
        self.resize(660, 400)
        self.handle_add_income = handle_add_income
        self.date_format = date_format
        self.add_income_frame()

    def add_income_frame(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(8, 8, 8, 8)
        self.setLayout(main_layout)
        self.add_income_card = QFrame()
        self.add_income_card.setStyleSheet("""
                    QFrame {
                        background-color: white;
                        border-radius: 10px;
                    }
                """)
        self.add_income_card.setFixedHeight(400)

        add_income_layout = QVBoxLayout()
        add_income_layout.setContentsMargins(10, 10, 10, 10)
        add_income_layout.setSpacing(4)
        self.add_income_card.setLayout(add_income_layout)

        row_one_layout = QHBoxLayout()
        row_one_layout.setContentsMargins(0, 10, 0, 0)
        row_one_layout.setSpacing(8)

        row_one_left_layout = QVBoxLayout()
        row_one_left_layout.setSpacing(4)

        income_category_label = QLabel("Income Category")
        income_category_label.setStyleSheet("""
                                   color: #334155;
                                   font-size: 13px;
                               """)

        self.income_category_input = QComboBox()
        self.income_category_input.setStyleSheet(get_combo_style())
        self.income_category_input.addItem("Salary", "salary")
        self.income_category_input.addItem("Bonus", "bonus")
        self.income_category_input.addItem("Freelance", "freelance")
        self.income_category_input.addItem("Benefits", "benefits")
        self.income_category_input.addItem("Rental Income", "rental income")
        self.income_category_input.addItem("Investment", "investment")
        self.income_category_input.addItem("Pension", "pension")
        self.income_category_input.addItem("Other", "other")
        self.income_category_input.setFixedHeight(36)

        row_one_left_layout.addWidget(income_category_label)
        row_one_left_layout.addWidget(self.income_category_input)

        row_one_middle_layout = QVBoxLayout()
        row_one_middle_layout.setSpacing(4)

        income_frequency_label = QLabel("Income Frequency")
        income_frequency_label.setStyleSheet("""
                                                                   color: #334155;
                                                                   font-size: 13px;
                                                               """)

        self.income_frequency_input = QComboBox()
        self.income_frequency_input.setStyleSheet(get_combo_style())
        self.income_frequency_input.addItem("Monthly", "monthly")
        self.income_frequency_input.addItem("Weekly", "weekly")
        self.income_frequency_input.addItem("Yearly", "yearly")
        self.income_frequency_input.addItem("Quarterly", "quarterly")
        self.income_frequency_input.addItem("One Off", "one off")
        self.income_frequency_input.setFixedHeight(36)

        self.income_frequency_input.currentTextChanged.connect(self.handle_is_recurring_value_changed)



        row_one_middle_layout.addWidget(income_frequency_label)
        row_one_middle_layout.addWidget(self.income_frequency_input)

        row_one_right_layout = QVBoxLayout()
        row_one_right_layout.setSpacing(4)

        received_date_label = QLabel("Date")
        received_date_label.setStyleSheet("""
                            color: #334155;
                            font-size: 13px;
                        """)

        self.received_date_input = PopupDateEdit()

        self.received_date_input.setCalendarPopup(True)
        self.received_date_input.setMaximumDate(QDate.currentDate())
        self.received_date_input.setDate(QDate.currentDate())
        self.set_current_date_format()
        self.received_date_input.lineEdit().setReadOnly(True)
        self.received_date_input.setEnabled(False)
        calendar = self.received_date_input.calendarWidget()
        calendar.setMinimumSize(360, 260)
        calendar.setStyleSheet(get_date_picker_style())

        self.received_date_input.setFixedHeight(36)
        self.received_date_input.setStyleSheet("""
                                    background-color: #f8fafc;
                                    border: 1px solid #e2e8f0;
                                    border-radius: 6px;
                                    padding: 0 10px;
                                    font-size: 14px;
                                """)


        row_one_right_layout.addWidget(received_date_label)
        row_one_right_layout.addWidget(self.received_date_input)

        row_one_layout.addLayout(row_one_left_layout, 1)
        row_one_layout.addLayout(row_one_middle_layout, 1)
        row_one_layout.addLayout(row_one_right_layout, 1)

        row_two_layout = QHBoxLayout()
        row_two_layout.setContentsMargins(0, 10, 0, 0)
        row_two_layout.setSpacing(8)

        row_two_left_layout = QVBoxLayout()
        row_two_left_layout.setSpacing(4)

        amount_label_layout = QHBoxLayout()
        amount_label_layout.setSpacing(4)

        amount_label = QLabel("Amount (£)")
        amount_label.setStyleSheet("""
                                  color: #334155;
                                  font-size: 13px;
                              """)

        self.amount_error = QLabel("")
        self.amount_error.setStyleSheet("""
                                           color: #ef4444;
                                           font-size: 13px;
                                       """)

        amount_label_layout.addWidget(amount_label)
        amount_label_layout.addWidget(self.amount_error)

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Enter amount")
        self.amount_input.setFixedHeight(36)
        self.amount_input.setStyleSheet("""
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

        row_two_left_layout.addLayout(amount_label_layout)
        row_two_left_layout.addWidget(self.amount_input)

        row_two_right_layout = QVBoxLayout()
        row_two_right_layout.setSpacing(4)

        source_name_label_layout = QHBoxLayout()
        source_name_label_layout.setSpacing(4)

        source_name_label = QLabel("Source Name")
        source_name_label.setStyleSheet("""
                                                         color: #334155;
                                                         font-size: 13px;
                                                     """)

        self.source_name_error = QLabel("")
        self.source_name_error.setStyleSheet("""
                                                                  color: #ef4444;
                                                                  font-size: 13px;
                                                              """)

        source_name_label_layout.addWidget(source_name_label)
        source_name_label_layout.addWidget(self.source_name_error)

        self.source_name_input = QLineEdit()
        self.source_name_input.setPlaceholderText("Enter income source name")
        self.source_name_input.setFixedHeight(36)
        self.source_name_input.setStyleSheet("""
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



        row_two_right_layout.addLayout(source_name_label_layout)
        row_two_right_layout.addWidget(self.source_name_input)

        notes_layout = QVBoxLayout()
        notes_layout.setContentsMargins(0, 10, 0, 10)
        notes_layout.setSpacing(8)

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
                               padding: 4px 10px;
                               font-size: 14px;
                           }
                           QTextEdit:focus {
                                   border: 1px solid #4f46e5;
                               }
                       """)

        notes_layout.addWidget(notes_label)
        notes_layout.addWidget(self.notes_input)

        row_two_layout.addLayout(row_two_left_layout, 1)
        row_two_layout.addLayout(row_two_right_layout, 1)

        self.add_income_notify_label = QLabel()
        self.add_income_notify_label.setWordWrap(True)
        self.add_income_notify_label.setStyleSheet("color: #22c55e;font-size: 14px;")

        button_row_layout = QHBoxLayout()
        button_row_layout.setContentsMargins(0, 20, 0, 0)
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

        self.submit_button = QPushButton("Add Income")
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

        self.submit_button.clicked.connect(self.handle_add_income_button_clicked)

        button_row_layout.addWidget(self.clear_button)
        button_row_layout.addWidget(self.submit_button)

        add_income_layout.addLayout(row_one_layout)
        add_income_layout.addLayout(row_two_layout)
        add_income_layout.addLayout(notes_layout)
        add_income_layout.addWidget(self.add_income_notify_label)
        add_income_layout.addLayout(button_row_layout)
        add_income_layout.addStretch()

        main_layout.addWidget(self.add_income_card)

    def handle_is_recurring_value_changed(self):

        if self.income_frequency_input.currentData() == "one off":
            self.received_date_input.setEnabled(True)
        else:
            self.received_date_input.setEnabled(False)

    def handle_add_income_button_clicked(self):
        if not self.validate_expense_form():
            return

        received_date = None

        if self.income_frequency_input.currentData() == "one off":
            received_date = self.received_date_input.date().toString("yyyy-MM-dd")

        income_data = {
            "category": self.income_category_input.currentData(),
            "amount": self.amount_input.text(),
            "source_name": self.source_name_input.text(),
            "frequency": self.income_frequency_input.currentData(),
            "notes": self.notes_input.toPlainText().strip() or None,
            "received_date": received_date
        }

        self.handle_add_income(income_data)

    def handle_clear_form(self):
        self.amount_input.setText("")
        self.notes_input.setText("")
        self.source_name_input.setText("")

    def validate_expense_form(self):

        self.amount_error.setText("")
        self.source_name_error.setText("")

        amount_text = self.amount_input.text().strip()
        source_name = self.source_name_input.text().strip()

        if not amount_text:
            self.amount_error.setText("Amount Is Required")
            return False

        try:
            amount = float(amount_text)
        except ValueError:
            self.amount_error.setText("Amount Must Be A Valid Number")
            return False

        if amount <= 0:
            self.amount_error.setText("Amount Must Be Greater Than 0")
            return False

        if not source_name:
            self.source_name_error.setText("Shop Name Is Required")
            return False

        return True

    def set_current_date_format(self,current_date_format = None):
        if current_date_format:
            self.date_format = current_date_format
        match self.date_format:
            case "YYYY-MM-DD":
                self.received_date_input.setDisplayFormat("yyyy-MM-dd")
            case "DD MMM YYYY":
                self.received_date_input.setDisplayFormat("dd MMM yyyy")
            case "DD/MM/YYYY":
                self.received_date_input.setDisplayFormat("dd/MM/yyyy")

