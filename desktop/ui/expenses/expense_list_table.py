from PySide6.QtWidgets import QTableWidget, QHeaderView


class ExpenseListTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.create_expense_list_table()

    def create_expense_list_table(self):

        self.setColumnCount(7)
        self.setHorizontalHeaderLabels([
            "Date", "Category", "Shop", "Amount", "Payment", "Type", "Notes"
        ])

        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.setAlternatingRowColors(True)

        self.setStyleSheet("""
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


            }
        """)