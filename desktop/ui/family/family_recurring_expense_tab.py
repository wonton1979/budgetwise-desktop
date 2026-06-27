from PySide6.QtWidgets import QFrame, QVBoxLayout, QHeaderView, QTableWidget

from ui.expenses.expense_list_table import ExpenseListTable


class FamilyRecurringExpensesTab(QFrame):
    def __init__(self):
        super().__init__()
        self.create_family_recurring_expenses_tab()

    def create_family_recurring_expenses_tab(self):
        self.setMinimumSize(800, 640)
        self.setStyleSheet("""
                    background-color: white;
                    border-top-left-radius: 0px;
                    border-top-right-radius: 10px;
                    border-bottom-left-radius: 10px;
                    border-bottom-right-radius: 10px;
                """)
        family_recurring_expense_list_card_layout = QVBoxLayout()
        family_recurring_expense_list_card_layout.setContentsMargins(20, 5, 20, 20)
        family_recurring_expense_list_card_layout.setSpacing(12)
        self.setLayout(family_recurring_expense_list_card_layout)
        self.create_family_recurring_expense_table()
        family_recurring_expense_list_card_layout.addWidget(self.table_list)



    def create_family_recurring_expense_table(self):
        self.table_list = QTableWidget()
        self.table_list.setColumnCount(6)
        self.table_list.setHorizontalHeaderLabels([
            "Owner", "Provider", "Sub Category", "Amount", "Frequency", "Notes"
        ])

        self.table_list.setColumnWidth(0, 120)
        self.table_list.setColumnWidth(1, 150)
        self.table_list.setColumnWidth(2, 180)
        self.table_list.setColumnWidth(3, 80)
        self.table_list.setColumnWidth(4, 100)
        self.table_list.horizontalHeader().setStretchLastSection(True)


        self.table_list.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table_list.setAlternatingRowColors(True)

        self.table_list.setStyleSheet("""
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
