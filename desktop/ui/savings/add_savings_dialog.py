from PySide6.QtCore import QDate
from PySide6.QtWidgets import QDialog, QFrame, QVBoxLayout, QHBoxLayout, QLabel, QDateEdit, QLineEdit, QPushButton, \
    QTextEdit

from utils.date_picker_style import get_date_picker_style


class AddSavingsDialog(QDialog):
    def __init__(self,handle_add_savings,date_format):
        super().__init__()
        self.savings_id = None
        self.setWindowTitle("Add Savings")
        self.setModal(True)
        self.resize(660, 370)
        self.handle_add_savings = handle_add_savings
        self.date_format = date_format
        self.add_savings_frame()

    def add_savings_frame(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(8, 8, 8, 8)
        self.setLayout(main_layout)

        self.add_savings_card = QFrame()
        self.add_savings_card.setStyleSheet("""
                       QFrame {
                           background-color: white;
                           border-radius: 10px;
                       }
                   """)
        self.add_savings_card.setFixedHeight(360)

        add_savings_layout = QVBoxLayout()
        add_savings_layout.setContentsMargins(10, 10, 10, 10)
        add_savings_layout.setSpacing(4)
        self.add_savings_card.setLayout(add_savings_layout)

        row_one_layout = QHBoxLayout()
        row_one_layout.setContentsMargins(0, 10, 0, 0)
        row_one_layout.setSpacing(8)

        row_one_left_layout = QVBoxLayout()
        row_one_left_layout.setSpacing(4)

        savings_name_label_layout = QHBoxLayout()
        savings_name_label_layout.setSpacing(4)

        savings_name_label = QLabel("Savings Name")
        savings_name_label.setStyleSheet("""
                                             color: #334155;
                                             font-size: 13px;
                                         """)

        self.savings_name_error = QLabel("")
        self.savings_name_error.setStyleSheet("""
                                                      color: #ef4444;
                                                      font-size: 10px;
                                                  """)

        savings_name_label_layout.addWidget(savings_name_label)
        savings_name_label_layout.addWidget(self.savings_name_error)

        self.savings_name_input = QLineEdit()
        self.savings_name_input.setPlaceholderText("Enter Savings Name")
        self.savings_name_input.setFixedHeight(36)
        self.savings_name_input.setStyleSheet("""
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

        row_one_left_layout.addLayout(savings_name_label_layout)
        row_one_left_layout.addWidget(self.savings_name_input)


        row_one_right_layout = QVBoxLayout()
        row_one_right_layout.setSpacing(4)

        goal_amount_label_layout = QHBoxLayout()
        goal_amount_label_layout.setSpacing(4)

        goal_amount_label = QLabel("Target Amount (£)")
        goal_amount_label.setStyleSheet("""
                                                    color: #334155;
                                                    font-size: 13px;
                                                """)

        self.goal_amount_error = QLabel("")
        self.goal_amount_error.setStyleSheet("""
                                                             color: #ef4444;
                                                             font-size: 10px;
                                                         """)

        goal_amount_label_layout.addWidget(goal_amount_label)
        goal_amount_label_layout.addWidget(self.goal_amount_error)

        self.goal_amount_input = QLineEdit()
        self.goal_amount_input.setPlaceholderText("Enter Amount")
        self.goal_amount_input.setFixedHeight(36)
        self.goal_amount_input.setStyleSheet("""
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



        row_one_right_layout.addLayout(goal_amount_label_layout)
        row_one_right_layout.addWidget(self.goal_amount_input)

        row_one_layout.addLayout(row_one_left_layout, 1)
        row_one_layout.addLayout(row_one_right_layout, 1)

        row_two_layout = QHBoxLayout()
        row_two_layout.setContentsMargins(0, 10, 0, 0)
        row_two_layout.setSpacing(8)

        row_two_left_layout = QVBoxLayout()
        row_two_left_layout.setSpacing(4)

        current_amount_label_layout = QHBoxLayout()
        current_amount_label_layout.setSpacing(4)

        current_amount_label = QLabel("Current Amount (£)")
        current_amount_label.setStyleSheet("""
                                                    color: #334155;
                                                    font-size: 13px;
                                                """)

        self.current_amount_error = QLabel("")
        self.current_amount_error.setStyleSheet("""
                                                             color: #ef4444;
                                                             font-size: 10px;
                                                         """)

        current_amount_label_layout.addWidget(current_amount_label)
        current_amount_label_layout.addWidget(self.current_amount_error)

        self.current_amount_input = QLineEdit()
        self.current_amount_input.setText("0.00")
        self.current_amount_input.setFixedHeight(36)
        self.current_amount_input.setStyleSheet("""
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

        row_two_left_layout.addLayout(current_amount_label_layout)
        row_two_left_layout.addWidget(self.current_amount_input)

        row_two_right_layout = QVBoxLayout()
        row_two_right_layout.setSpacing(4)

        target_date_label = QLabel("Target Date")
        target_date_label.setStyleSheet("""
                                          color: #334155;
                                          font-size: 13px;
                                      """)
        tomorrow = QDate.currentDate().addDays(1)
        self.target_date_input = QDateEdit()
        self.target_date_input.setMinimumDate(tomorrow)
        self.target_date_input.setSpecialValueText("No Target Date")
        self.target_date_input.setDate(self.target_date_input.minimumDate())
        self.set_current_date_format()
        self.target_date_input.setCalendarPopup(True)
        self.target_date_input.lineEdit().setReadOnly(True)
        target_date_calendar = self.target_date_input.calendarWidget()
        target_date_calendar.setMinimumSize(360, 260)
        target_date_calendar.setStyleSheet(get_date_picker_style())

        self.target_date_input.setFixedHeight(36)
        self.target_date_input.setStyleSheet("""
                                                  background-color: #f8fafc;
                                                  border: 1px solid #e2e8f0;
                                                  border-radius: 6px;
                                                  padding: 0 10px;
                                                  font-size: 14px;
                                              """)


        row_two_right_layout.addWidget(target_date_label)
        row_two_right_layout.addWidget(self.target_date_input)

        row_two_layout.addLayout(row_two_left_layout, 1)
        row_two_layout.addLayout(row_two_right_layout, 1)

        notes_label = QLabel("Notes (Optional)")
        notes_label.setStyleSheet("""
                                      color: #334155;
                                      font-size: 13px;
                                  """)

        row_three_layout = QHBoxLayout()
        row_three_layout.setContentsMargins(0, 10, 0, 0)
        row_three_layout.setSpacing(8)

        notes_layout = QVBoxLayout()
        notes_layout.setSpacing(4)

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

        row_three_layout.addLayout(notes_layout)

        self.add_savings_notify_label = QLabel()
        self.add_savings_notify_label.setWordWrap(True)
        self.add_savings_notify_label.setStyleSheet("color: #22c55e;font-size: 14px;")

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

        self.submit_button = QPushButton("Add Savings")
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

        self.submit_button.clicked.connect(self.handle_add_savings_button_clicked)

        button_row_layout.addWidget(self.clear_button)
        button_row_layout.addWidget(self.submit_button)

        add_savings_layout.addLayout(row_one_layout)
        add_savings_layout.addLayout(row_two_layout)
        add_savings_layout.addLayout(row_three_layout)
        add_savings_layout.addWidget(self.add_savings_notify_label)
        add_savings_layout.addLayout(button_row_layout)
        add_savings_layout.addStretch()

        main_layout.addWidget(self.add_savings_card)

    def handle_clear_form(self):
        self.savings_name_input.setText("")
        self.goal_amount_input.setText("")
        self.current_amount_input.setText("0.00")
        self.notes_input.setPlainText("")

    def validate_add_savings_form(self):

        self.goal_amount_error.setText("")
        self.savings_name_error.setText("")
        self.current_amount_error.setText("")

        goal_amount_text = self.goal_amount_input.text().strip()
        current_amount_text = self.current_amount_input.text().strip()
        savings_name = self.savings_name_input.text().strip()

        if not goal_amount_text:
            self.goal_amount_error.setText("Amount Is Required")
            return False

        if not current_amount_text:
            self.current_amount_error.setText("Amount Is Required")
            return False

        try:
            goal_amount = float(goal_amount_text)
        except ValueError:
            self.goal_amount_error.setText("Amount Must Be A Valid Number")
            return False

        try:
            current_amount = float(current_amount_text)
        except ValueError:
            self.current_amount_error.setText("Amount Must Be A Valid Number")
            return False

        if goal_amount <= 0:
            self.goal_amount_error.setText("Amount Must Be Greater Than Zero")
            return False

        if current_amount < 0:
            self.current_amount_error.setText("Amount Can't Be Negative")
            return False

        if not savings_name:
            self.savings_name_error.setText("Savings Name Is Required")
            return False

        return True

    def handle_add_savings_button_clicked(self):
        if not self.validate_add_savings_form():
            return

        savings_data = {
            "purpose_name": self.savings_name_input.text().strip(),
            "goal_amount": float(self.goal_amount_input.text()),
            "current_amount": float(self.current_amount_input.text()),
            "target_date": self.target_date_input.date().toString(
                "yyyy-MM-dd") if self.target_date_input.date() != self.target_date_input.minimumDate() else None,
            "notes": self.notes_input.toPlainText().strip() or None
        }

        self.handle_add_savings(savings_data)

    def set_current_date_format(self,current_date_format = None):
        if current_date_format:
            self.date_format = current_date_format
        match self.date_format:
            case "YYYY-MM-DD":
                self.target_date_input.setDisplayFormat("yyyy-MM-dd")
            case "DD MMM YYYY":
                self.target_date_input.setDisplayFormat("dd MMM yyyy")
            case "DD/MM/YYYY":
                self.target_date_input.setDisplayFormat("dd/MM/yyyy")

