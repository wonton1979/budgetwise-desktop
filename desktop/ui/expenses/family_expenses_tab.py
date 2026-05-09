from PySide6.QtWidgets import QFrame, QVBoxLayout

from ui.expenses.expense_list_table import ExpenseListTable
from ui.expenses.expenses_bottom_bar import ExpenseBottomBar
from ui.expenses.expenses_filter import ExpensesFilter


class FamilyExpensesTab(QFrame):
    def __init__(self,handle_on_search):
        super().__init__()
        self.handle_on_search = handle_on_search
        self.create_family_expenses_tab()

    def create_family_expenses_tab(self):

        self.setStyleSheet("""
                    background-color: white;
                    border-top-left-radius: 0px;
                    border-top-right-radius: 10px;
                    border-bottom-left-radius: 10px;
                    border-bottom-right-radius: 10px;
                """)
        family_expense_list_card_layout = QVBoxLayout()
        family_expense_list_card_layout.setContentsMargins(20, 5, 20, 20)
        family_expense_list_card_layout.setSpacing(12)
        self.setLayout(family_expense_list_card_layout)

        self.family_expense_filter = ExpensesFilter(self.handle_on_search)
        self.family_expense_list_table = ExpenseListTable()



        family_expense_list_card_layout.addWidget(self.family_expense_filter)
        family_expense_list_card_layout.addWidget(self.family_expense_list_table)

