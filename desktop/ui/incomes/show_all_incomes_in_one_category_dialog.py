from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QVBoxLayout, QFrame, QTableWidget, QHeaderView, QTableWidgetItem

from ui.incomes.edit_income_dialog import EditIncomeDialog
from utils.date_format_convertor import uk_date_format, long_date_format


class ShowAllIncomesDialog(QDialog):
    def __init__(self,handle_edit_income,handle_delete_income,fetch_single_income_by_income_id,incomes_data,currency_symbol,date_format):
        super().__init__()
        self.incomes_data = incomes_data
        self.date_format = date_format
        self.currency_symbol = currency_symbol
        self.handle_update_income = handle_edit_income
        self.handle_delete_income = handle_delete_income
        self.fetch_single_income_by_income_id = fetch_single_income_by_income_id
        self.setWindowTitle("Show all incomes")
        self.setFixedSize(1000,600)
        self.setModal(True)
        self.show_all_incomes_frame()

    def show_all_incomes_frame(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(8, 8, 8, 8)
        self.setLayout(main_layout)

        self.incomes_frame = QFrame()
        self.incomes_frame.setStyleSheet("background-color: white;border-radius: 10px;")
        self.incomes_frame.setFixedHeight(600)

        incomes_frame_layout = QVBoxLayout()
        incomes_frame_layout.setContentsMargins(10, 10, 10, 10)
        incomes_frame_layout.setSpacing(4)
        self.incomes_frame.setLayout(incomes_frame_layout)

        self.incomes_table = QTableWidget()
        self.incomes_table.setColumnCount(7)
        self.incomes_table.setHorizontalHeaderLabels([
            "id", "Amount", "Category", "Frequency", "Source Name", "Received Date", "Notes",
        ])
        self.incomes_table.setColumnHidden(0, True)
        self.incomes_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: none;
                gridline-color: #e2e8f0;
                font-size: 13px;
            }

            QHeaderView::section {
                background-color: #e2e8f0;
                color: #0f172a;
                font-weight: 600;
                padding: 10px;
                border: none;
                border-bottom: 1px solid #cbd5e1;
            }
        """)
        self.incomes_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.incomes_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.incomes_table.setAlternatingRowColors(True)
        self.incomes_table.cellDoubleClicked.connect(self.handle_edit_income)

        incomes_frame_layout.addWidget(self.incomes_table)

        main_layout.addWidget(self.incomes_frame)
        self.load_table_data()

    def load_table_data(self):
        self.incomes_table.setRowCount(len(self.incomes_data))
        for row, each_income in enumerate(self.incomes_data):
            if row <= 20:
                income_id = QTableWidgetItem(str(each_income["id"]))
                self.incomes_table.setItem(row, 0, income_id)

                amount = QTableWidgetItem(f"{self.currency_symbol}" + str(each_income["amount"]))
                amount.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                self.incomes_table.setItem(row, 1, amount)

                income_category = QTableWidgetItem(each_income["category"].title() or "")
                income_category.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.incomes_table.setItem(row, 2, income_category)

                frequency = QTableWidgetItem(each_income["frequency"].title() or "")
                frequency.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.incomes_table.setItem(row, 3, frequency)

                source_name = QTableWidgetItem(each_income["source_name"])
                source_name.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.incomes_table.setItem(row, 4, source_name)

                received_date_display = each_income["received_date"]
                match self.date_format:
                    case "DD/MM/YYYY":
                        received_date_display = uk_date_format(str(each_income["received_date"]))
                    case "DD MMM YYYY":
                        received_date_display = long_date_format(str(each_income["received_date"]))
                received_date_date = QTableWidgetItem(received_date_display)
                received_date_date.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                self.incomes_table.setItem(row, 5, QTableWidgetItem(received_date_date))

                income_notes = QTableWidgetItem(each_income["notes"].title() if each_income["notes"] else "")
                income_notes.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.incomes_table.setItem(row, 6, income_notes)


    def handle_edit_income(self,row):

        response =self.fetch_single_income_by_income_id(int(self.incomes_table.item(row, 0).text()))["data"]
        income_details = {
            "id": response["id"],
            "amount": response["amount"],
            "category": response["category"],
            "frequency": response["frequency"],
            "source_name": response["source_name"],
            "received_date": response["received_date"],
            "notes": response["notes"],
        }
        self.update_income_dialog = EditIncomeDialog(self.handle_update_income,
                                                     self.handle_delete_income,
                                                     income_details,
                                                     self.date_format
                                                     )
        self.update_income_dialog.exec()







