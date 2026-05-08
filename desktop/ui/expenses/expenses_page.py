from PySide6.QtCore import QDate
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QTabWidget, QPushButton, QHBoxLayout, QLabel, \
    QTableWidgetItem, QHeaderView, QTableWidget

from services.expense_service import get_expenses
from ui.expenses.add_expense_card import AddExpenseCard
from ui.expenses.expenses_bottom_bar import ExpenseBottomBar
from ui.expenses.expenses_filter import ExpensesFilter



class ExpensesPage(QWidget):
    def __init__(self,access_token_getter):
        super().__init__()
        self.get_access_token = access_token_getter
        self.create_expenses_page()
        self.current_page = 1
        self.page_limit = 8
        self.total_pages = 1
        self.current_filter = {}

    def create_expenses_page(self):

        expense_page_layout = QVBoxLayout()
        expense_page_layout.setContentsMargins(0, 0, 0, 0)
        expense_page_layout.setSpacing(16)
        self.setLayout(expense_page_layout)

        self.expense_list_card = QFrame()
        self.expense_list_card.setStyleSheet("""
            background-color: white;
            border-top-left-radius: 0px;
            border-top-right-radius: 10px;
            border-bottom-left-radius: 10px;
            border-bottom-right-radius: 10px;
        """)

        expense_list_card_layout = QVBoxLayout()
        expense_list_card_layout.setContentsMargins(20, 5, 20, 20)
        expense_list_card_layout.setSpacing(12)
        self.expense_list_card.setLayout(expense_list_card_layout)

        self.expense_tabs = QTabWidget()
        self.expense_tabs.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                top: -1px;
            }

            QTabBar::tab {
                background: #1e293b;
                color: #ffffff;
                padding: 8px 16px;
                margin-right: 4px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }

            QTabBar::tab:selected {
                background: #ffffff;
                color: #000000;
                font-weight: 600;
            }

            QTabBar::tab:!selected:hover {
                background: #334155;
                color: #ffffff;
            }
        """)

        self.expense_filter = ExpensesFilter(self.handle_on_search)

        self.create_expense_list_table()

        self.expense_bottom_bar = ExpenseBottomBar(self.handle_load_expenses,self.get_current_filter)

        self.add_expense_card = AddExpenseCard(self.get_access_token, self.handle_load_expenses)


        expense_list_card_layout.addWidget(self.expense_filter)
        expense_list_card_layout.addWidget(self.expense_table)
        expense_list_card_layout.addWidget(self.expense_bottom_bar)

        self.expense_tabs.addTab(self.expense_list_card, "Expenses")
        self.expense_tabs.addTab(self.add_expense_card, "Add Expense")

        expense_page_layout.addWidget(self.expense_tabs)

        expense_page_layout.addStretch()


    def handle_load_expenses(self,payment_method=None,shopping_type=None,category=None,min_amount=None,max_amount=None,
                             start_date=None, end_date=None,sort_by=None,order=None,current_page=1,page_limit=8):
        if not start_date:
            start_date = QDate( QDate.currentDate().year(),QDate.currentDate().month(),1).toString("yyyy-MM-dd")

        response = get_expenses(self.get_access_token(),payment_method,shopping_type,category,min_amount,max_amount,
                                start_date, end_date,sort_by,order,current_page,page_limit)

        total = response["total"]
        page = response["page"] or 1
        total_pages = response["total_pages"] or 1

        self.current_page = page
        self.total_pages = total_pages

        self.expense_table.setRowCount(len(response["data"]))

        for row,each_expense in enumerate(response["data"]):

            expense_date = QTableWidgetItem(each_expense["expense_date"])
            expense_date.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.expense_table.setItem(row, 0, QTableWidgetItem(each_expense["expense_date"]))

            shop_category = QTableWidgetItem(each_expense["category"].title())
            shop_category.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.expense_table.setItem(row, 1, shop_category)

            shop_name = QTableWidgetItem(each_expense["shop_name"])
            shop_name.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.expense_table.setItem(row, 2, shop_name)

            amount = QTableWidgetItem("£"+each_expense["amount"])
            amount.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.expense_table.setItem(row, 3, amount)

            payment = QTableWidgetItem(each_expense["payment_method"].title())
            payment.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.expense_table.setItem(row, 4, payment)

            shopping_type = QTableWidgetItem(each_expense["shopping_type"].title())
            shopping_type.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.expense_table.setItem(row, 5, shopping_type)

            self.expense_table.setItem(row, 6, QTableWidgetItem(each_expense["notes"] or ""))

        self.expense_bottom_bar.expense_result_label.setText(
            f"Found {total} records | Page {page} of {total_pages}"
        )
        self.expense_bottom_bar.total_pages = total_pages
        self.expense_bottom_bar.prev_page_button.setEnabled(page > 1)
        self.expense_bottom_bar.next_page_button.setEnabled(page < total_pages)

    def create_expense_list_table(self):
        self.expense_table = QTableWidget()
        self.expense_table.setColumnCount(7)
        self.expense_table.setHorizontalHeaderLabels([
            "Date", "Category", "Shop", "Amount", "Payment", "Type", "Notes"
        ])

        self.expense_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.expense_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.expense_table.setAlternatingRowColors(True)

        self.expense_table.setStyleSheet("""
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

    def handle_on_search(self,payment_method=None,shopping_type=None,category=None,min_amount=None,max_amount=None,
                             start_date=None, end_date=None,sort_by=None,order=None):
        self.current_filter["payment_method"] = payment_method
        self.current_filter["shopping_type"] = shopping_type
        self.current_filter["category"] = category
        self.current_filter["min_amount"] = min_amount
        self.current_filter["max_amount"] = max_amount
        self.current_filter["start_date"] = start_date
        self.current_filter["end_date"] = end_date
        self.current_filter["sort_by"] = sort_by
        self.current_filter["order"] = order

        self.handle_load_expenses(
            self.current_filter["payment_method"],
            self.current_filter["shopping_type"],
            self.current_filter["category"],
            self.current_filter["min_amount"],
            self.current_filter["max_amount"],
            self.current_filter["start_date"],
            self.current_filter["end_date"],
            self.current_filter["sort_by"],
            self.current_filter["order"]
        )


    def create_group_widget(self):

        group_widget = QWidget()
        group_widget_layout = QVBoxLayout()
        group_widget_layout.setSpacing(4)
        group_widget_layout.setContentsMargins(0, 0, 0, 0)
        group_widget.setLayout(group_widget_layout)

        return group_widget


    def get_combo_style(self):
        return """
               QComboBox {
                   background-color: #f8fafc;
                   border: 1px solid #e2e8f0;
                   border-radius: 6px;
                   padding: 0 10px;
                   font-size: 14px;
               }

               QComboBox QAbstractItemView {
                   background-color: white;
                   border: 1px solid #e2e8f0;
                   selection-background-color: #e2e8f0;
               }
           """

    def get_current_filter(self):
        return self.current_filter