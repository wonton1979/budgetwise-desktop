import requests
from PySide6.QtCore import QDate, QTimer
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QTableWidgetItem, QLabel, QHBoxLayout

from services.expense_service import get_expenses, get_expense_by_id, update_expense, \
    delete_expense, add_expense
from ui.components.dialogs.message_dialog import MessageDialog
from ui.expenses.add_expense_dialog import AddExpenseDialog
from ui.expenses.edit_expense_dialog import EditExpenseDialog
from ui.expenses.expense_list_table import ExpenseListTable
from ui.expenses.expenses_bottom_bar import ExpenseBottomBar
from ui.components.expenses_filter import ExpenseFilterPanel
from utils.date_format_convertor import uk_date_format,long_date_format


class ExpensesPage(QWidget):
    def __init__(self,access_token_getter,handle_token_expired,currency_symbol,date_format):
        super().__init__()
        self.get_access_token = access_token_getter

        self.current_page = 1
        self.family_current_page =1
        self.currency_symbol = currency_symbol
        self.date_format = date_format
        self.page_limit = 8
        self.total_pages = 1
        self.current_filter: dict[str, str | None] = {
            "payment_method": None,
            "shopping_type": None,
            "category": None,
            "min_amount": None,
            "max_amount": None,
            "start_date": None,
            "end_date": None,
            "sort_by": None,
            "order": None
        }

        self.handle_token_expired = handle_token_expired
        self.create_expenses_page()

    def create_expenses_page(self):

        expense_page_layout = QVBoxLayout()
        expense_page_layout.setContentsMargins(0, 0, 0, 0)
        expense_page_layout.setSpacing(16)
        self.setLayout(expense_page_layout)

        self.expense_list_card = QFrame()
        self.expense_list_card.setStyleSheet("""
            background-color: white;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
            border-bottom-left-radius: 10px;
            border-bottom-right-radius: 10px;
        """)

        expense_list_card_layout = QVBoxLayout()
        expense_list_card_layout.setContentsMargins(20, 5, 20, 20)
        expense_list_card_layout.setSpacing(12)
        self.expense_list_card.setLayout(expense_list_card_layout)


        self.expense_filter = ExpenseFilterPanel(self.handle_on_search,self.date_format)

        self.expense_table = ExpenseListTable(handle_edit_expense=self.handle_edit_expense)

        self.add_expense_dialog = AddExpenseDialog(handler_add_expense=self.handle_add_expense,
                                                   date_format=self.date_format)

        label_group_layout = QHBoxLayout()
        label_group_layout.setSpacing(4)
        label_group_layout.setContentsMargins(0, 0, 0, 0)

        self.edit_expense_tips_label = QLabel("Tip: Double-Click An Expense To Edit")

        self.load_expenses_error_label = QLabel("")

        label_group_layout.addWidget(self.edit_expense_tips_label)
        label_group_layout.addWidget(self.load_expenses_error_label)

        self.edit_expense_tips_label.setStyleSheet("color: #4f46e5;font-size: 12px; font-weight: 600;")

        self.expense_bottom_bar = ExpenseBottomBar(self.handle_previous_page,self.handle_next_page)


        expense_list_card_layout.addWidget(self.expense_filter)
        expense_list_card_layout.addWidget(self.expense_table)
        expense_list_card_layout.addLayout(label_group_layout)
        expense_list_card_layout.addWidget(self.expense_bottom_bar)

        expense_page_layout.addWidget(self.expense_list_card)


    def handle_load_expenses(self,payment_method=None,shopping_type=None,category=None,min_amount=None,max_amount=None,
                             start_date=None, end_date=None,sort_by=None,order=None,current_page=1,page_limit=8,currency_symbol=None,date_format=None):
        if currency_symbol:
            self.currency_symbol = currency_symbol

        if date_format:
            self.date_format = date_format

        if not start_date:
            start_date = QDate( QDate.currentDate().year(),QDate.currentDate().month(),1).toString("yyyy-MM-dd")

        try:
            response = get_expenses(self.get_access_token(),payment_method,shopping_type,category,min_amount,max_amount,
                                start_date, end_date,sort_by,order,current_page,page_limit)
            total = response["total"]
            page = response["page"] or 1
            total_pages = response["total_pages"] or 1

            self.current_page = page
            self.total_pages = total_pages

            self.expense_table.setRowCount(len(response["data"]))

            for row, each_expense in enumerate(response["data"]):
                expense_id = QTableWidgetItem(str(each_expense["id"]))
                self.expense_table.setItem(row, 0, expense_id)
                expense_date_display = str(each_expense["expense_date"])

                match self.date_format:
                    case "DD/MM/YYYY":
                        expense_date_display = uk_date_format(str(each_expense["expense_date"]))
                    case "DD MMM YYYY":
                        expense_date_display = long_date_format(str(each_expense["expense_date"]))


                expense_date = QTableWidgetItem(expense_date_display)
                expense_date.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.expense_table.setItem(row, 1, expense_date)

                shop_category = QTableWidgetItem(each_expense["category"].title())
                shop_category.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.expense_table.setItem(row, 2, shop_category)

                shop_name = QTableWidgetItem(each_expense["shop_name"])
                shop_name.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.expense_table.setItem(row, 3, shop_name)

                amount = QTableWidgetItem(f"{self.currency_symbol}" + each_expense["amount"])
                amount.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                self.expense_table.setItem(row, 4, amount)

                payment = QTableWidgetItem(each_expense["payment_method"].title())
                payment.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.expense_table.setItem(row, 5, payment)

                shopping_type = QTableWidgetItem(each_expense["shopping_type"].title())
                shopping_type.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.expense_table.setItem(row, 6, shopping_type)

                expense_notes = QTableWidgetItem(each_expense["notes"] or "")
                expense_notes.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.expense_table.setItem(row, 7, expense_notes)

            self.expense_bottom_bar.expense_result_label.setText(
                f"Found {total} records | Page {page} of {total_pages}"
            )
            self.expense_bottom_bar.total_pages = total_pages
            self.expense_bottom_bar.prev_page_button.setEnabled(page > 1)
            self.expense_bottom_bar.next_page_button.setEnabled(page < total_pages)


        except requests.ConnectionError:

            connection_error_message_dialog = MessageDialog("Connection Error", "Unable to connect to the server.")

            connection_error_message_dialog.error_dialog()

            connection_error_message_dialog.exec()


        except requests.Timeout:

            timeout_error_message_dialog = MessageDialog("Connection Error", "The request timed out.")

            timeout_error_message_dialog.error_dialog()

            timeout_error_message_dialog.exec()


        except Exception as error:

            api_error_message_dialog = MessageDialog("API Error", str(error))

            api_error_message_dialog.error_dialog()

            api_error_message_dialog.exec()

            if str(error) == "Session Expired":
                self.handle_token_expired()

    def handle_add_expense(self,expense_data):
        try:
            add_expense(expense_data, self.get_access_token())
            self.add_expense_dialog.add_expense_notify_label.setText("Successfully Added Expense")
            self.add_expense_dialog.amount_input.setText("")
            self.add_expense_dialog.shop_name_input.setText("")
            self.add_expense_dialog.tag_input.setText("")
            self.add_expense_dialog.notes_input.setPlainText("")
            self.handle_load_expenses()
            QTimer.singleShot(2000, self.add_expense_dialog.reject)


        except requests.ConnectionError:
            connection_error_message_dialog = MessageDialog("Connection Error", "Unable to connect to the server.")
            connection_error_message_dialog.error_dialog()
            connection_error_message_dialog.exec()

        except requests.Timeout:
            timeout_error_message_dialog = MessageDialog("Connection Error", "The request timed out.")
            timeout_error_message_dialog.error_dialog()
            timeout_error_message_dialog.exec()

        except Exception as error:
            api_error_message_dialog = MessageDialog("API Error", str(error))
            api_error_message_dialog.error_dialog()
            api_error_message_dialog.exec()

            if str(error) == "Session Expired":
                self.handle_token_expired()


    def handle_previous_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            if self.current_filter:
                self.handle_load_expenses(
                    self.current_filter["payment_method"],
                    self.current_filter["shopping_type"],
                    self.current_filter["category"],
                    self.current_filter["min_amount"],
                    self.current_filter["max_amount"],
                    self.current_filter["start_date"],
                    self.current_filter["end_date"],
                    self.current_filter["sort_by"],
                    self.current_filter["order"],
                    current_page=self.current_page,
                    page_limit=self.page_limit
                )
            else:
                self.handle_load_expenses(
                    current_page=self.current_page,
                    page_limit=self.page_limit
                )

    def handle_next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            if self.current_filter:
                self.handle_load_expenses(
                    self.current_filter["payment_method"],
                    self.current_filter["shopping_type"],
                    self.current_filter["category"],
                    self.current_filter["min_amount"],
                    self.current_filter["max_amount"],
                    self.current_filter["start_date"],
                    self.current_filter["end_date"],
                    self.current_filter["sort_by"],
                    self.current_filter["order"],
                    current_page=self.current_page,
                    page_limit=self.page_limit
                )
            else:
                self.handle_load_expenses(
                    current_page=self.current_page,
                    page_limit=self.page_limit
                )

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



    def get_current_filter(self):
        return self.current_filter

    def handle_edit_expense(self,row):
        expense_id_text = self.expense_table.item(row,0)
        if expense_id_text:
            existing_payload = get_expense_by_id(int(expense_id_text.text()),self.get_access_token())
            self.edit_expense_dialog = EditExpenseDialog(self.handle_update_expense,self.handle_delete_expense,
                                                         existing_payload["data"],self.date_format)
            self.edit_expense_dialog.exec()

    def handle_update_expense(self,expense_id,expense_data):
        try:
            update_expense(int(expense_id),expense_data,self.get_access_token())
            self.handle_load_expenses(
                self.current_filter["payment_method"],
                self.current_filter["shopping_type"],
                self.current_filter["category"],
                self.current_filter["min_amount"],
                self.current_filter["max_amount"],
                self.current_filter["start_date"],
                self.current_filter["end_date"],
                self.current_filter["sort_by"],
                self.current_filter["order"],
                current_page=self.current_page,
                page_limit=self.page_limit
            )

        except requests.ConnectionError:
            connection_error_message_dialog = MessageDialog("Connection Error", "Unable to connect to the server.")
            connection_error_message_dialog.error_dialog()
            connection_error_message_dialog.exec()

        except requests.Timeout:
            timeout_error_message_dialog = MessageDialog("Connection Error", "The request timed out.")
            timeout_error_message_dialog.error_dialog()
            timeout_error_message_dialog.exec()

        except Exception as error:
            api_error_message_dialog = MessageDialog("API Error", str(error))
            api_error_message_dialog.error_dialog()
            api_error_message_dialog.exec()

            if str(error) == "Session Expired":
                self.handle_token_expired()

    def handle_delete_expense(self,expense_id):
        try:
            delete_expense(int(expense_id),self.get_access_token())
            self.handle_load_expenses(
                self.current_filter["payment_method"],
                self.current_filter["shopping_type"],
                self.current_filter["category"],
                self.current_filter["min_amount"],
                self.current_filter["max_amount"],
                self.current_filter["start_date"],
                self.current_filter["end_date"],
                self.current_filter["sort_by"],
                self.current_filter["order"],
                current_page=self.current_page,
                page_limit=self.page_limit
            )
        except requests.ConnectionError:
            connection_error_message_dialog = MessageDialog("Connection Error", "Unable to connect to the server.")
            connection_error_message_dialog.error_dialog()
            connection_error_message_dialog.exec()

        except requests.Timeout:
            timeout_error_message_dialog = MessageDialog("Connection Error", "The request timed out.")
            timeout_error_message_dialog.error_dialog()
            timeout_error_message_dialog.exec()

        except Exception as error:
            api_error_message_dialog = MessageDialog("API Error", str(error))
            api_error_message_dialog.error_dialog()
            api_error_message_dialog.exec()

            if str(error) == "Session Expired":
                self.handle_token_expired()
