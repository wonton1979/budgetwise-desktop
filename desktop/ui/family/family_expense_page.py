import requests
from PySide6.QtCore import QDate
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QTabWidget, QTableWidgetItem

from services.family_service import get_family_expenses,get_family_recurring_expenses
from ui.components.dialogs.message_dialog import MessageDialog
from ui.family.family_expenses_tab import FamilyExpensesTab
from ui.family.family_recurring_expense_tab import FamilyRecurringExpensesTab
from utils.date_format_convertor import uk_date_format, long_date_format


class FamilyExpensesPage(QWidget):
    def __init__(self,access_token_getter,handle_token_expired,currency_symbol,date_format):
        super().__init__()
        self.get_access_token = access_token_getter
        self.family_current_page =1
        self.page_limit = 8
        self.total_pages = 1
        self.currency_symbol = currency_symbol
        self.date_format = date_format
        self.current_family_filter: dict[str, str | int | float | None] = {
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
        self.create_family_expenses_page()

    def create_family_expenses_page(self):

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

        self.family_expenses_tab = FamilyExpensesTab(
                                                    self.handle_on_family_search,
                                                    self.handle_family_previous_page,
                                                    self.handle_family_next_page,self.date_format
                                                   )


        self.family_recurring_expense_tab = FamilyRecurringExpensesTab()

        self.expense_tabs.addTab(self.family_expenses_tab, "Family Expenses")
        self.expense_tabs.addTab(self.family_recurring_expense_tab, "Family Recurring Expenses")



        expense_page_layout.addWidget(self.expense_tabs)


    def handle_load_family_expenses(self,payment_method=None,shopping_type=None,category=None,min_amount=None,max_amount=None,
                             start_date=None, end_date=None,sort_by=None,order=None,current_page=1,page_limit=8,
                                    currency_symbol=None,new_date_format=None):
        if currency_symbol:
            self.currency_symbol = currency_symbol

        if new_date_format:
            self.date_format = new_date_format

        if not start_date:
            start_date = QDate( QDate.currentDate().year(),QDate.currentDate().month(),1).toString("yyyy-MM-dd")

        self.current_family_filter["payment_method"] = payment_method
        self.current_family_filter["shopping_type"] = shopping_type
        self.current_family_filter["category"] = category
        self.current_family_filter["min_amount"] = min_amount
        self.current_family_filter["max_amount"] = max_amount
        self.current_family_filter["start_date"] = start_date
        self.current_family_filter["end_date"] = end_date
        self.current_family_filter["sort_by"] = sort_by
        self.current_family_filter["order"] = order

        try:
            response = get_family_expenses(self.get_access_token(), payment_method, shopping_type, category, min_amount,
                                           max_amount,
                                           start_date, end_date, sort_by, order, current_page, page_limit)

            total = response["total"]
            page = response["page"] or 1
            total_pages = response["total_pages"] or 1

            self.current_page = page
            self.total_pages = total_pages

            self.family_expenses_tab.family_expense_list_table.setRowCount(len(response["data"]))

            for row, each_expense in enumerate(response["data"]):
                expense_id = QTableWidgetItem(each_expense["id"])
                self.family_expenses_tab.family_expense_list_table.setItem(row, 0, expense_id)
                expense_date_display = each_expense["expense_date"]
                match self.date_format:
                    case "DD/MM/YYYY":
                        expense_date_display = uk_date_format(str(each_expense["expense_date"]))
                    case "DD MMM YYYY":
                        expense_date_display = long_date_format(str(each_expense["expense_date"]))
                expense_date = QTableWidgetItem(expense_date_display)
                expense_date.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                self.family_expenses_tab.family_expense_list_table.setItem(row, 1, QTableWidgetItem(
                    expense_date))

                shop_category = QTableWidgetItem(each_expense["category"].title() or "")
                shop_category.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.family_expenses_tab.family_expense_list_table.setItem(row, 2, shop_category)

                shop_name = QTableWidgetItem(each_expense["shop_name"])
                shop_name.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.family_expenses_tab.family_expense_list_table.setItem(row, 3, shop_name)

                amount = QTableWidgetItem(f"{self.currency_symbol}" + each_expense["amount"])
                amount.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                self.family_expenses_tab.family_expense_list_table.setItem(row, 4, amount)

                payment = QTableWidgetItem(each_expense["payment_method"].title() if each_expense["payment_method"] else "")
                payment.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.family_expenses_tab.family_expense_list_table.setItem(row, 5, payment)

                shopping_type = QTableWidgetItem(each_expense["shopping_type"].title() if each_expense["shopping_type"] else "")
                shopping_type.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.family_expenses_tab.family_expense_list_table.setItem(row, 6, shopping_type)

                shopping_notes = QTableWidgetItem(each_expense["notes"].title() if each_expense["notes"] else "")
                shopping_notes.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.family_expenses_tab.family_expense_list_table.setItem(row, 7, shopping_notes)

                spend_by = QTableWidgetItem(each_expense["display_name"].title() if each_expense["display_name"] else "")
                spend_by.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.family_expenses_tab.family_expense_list_table.setItem(row, 8, spend_by)

            self.family_expenses_tab.family_expense_bottom_bar.expense_result_label.setText(
                f"Found {total} records | Page {page} of {total_pages}"
            )
            self.family_expenses_tab.family_expense_bottom_bar.total_pages = total_pages
            self.family_expenses_tab.family_expense_bottom_bar.prev_page_button.setEnabled(page > 1)
            self.family_expenses_tab.family_expense_bottom_bar.next_page_button.setEnabled(page < total_pages)



        except requests.ConnectionError:

            connection_error_message_dialog = MessageDialog("Connection Error", "Unable to connect to the server.")

            connection_error_message_dialog.error_dialog()

            connection_error_message_dialog.exec()


        except requests.Timeout:

            timeout_error_message_dialog = MessageDialog("Connection Error", "The request timed out.")

            timeout_error_message_dialog.error_dialog()

            timeout_error_message_dialog.exec()


        except Exception as error:

            if str(error) == "Session Expired":
                self.handle_token_expired()

            api_error_message_dialog = MessageDialog("API Error", str(error))

            api_error_message_dialog.error_dialog()

            api_error_message_dialog.exec()


    def handle_on_family_search(self,payment_method=None,shopping_type=None,category=None,min_amount=None,max_amount=None,
                             start_date=None, end_date=None,sort_by=None,order=None):
        self.current_family_filter["payment_method"] = payment_method
        self.current_family_filter["shopping_type"] = shopping_type
        self.current_family_filter["category"] = category
        self.current_family_filter["min_amount"] = min_amount
        self.current_family_filter["max_amount"] = max_amount
        self.current_family_filter["start_date"] = start_date
        self.current_family_filter["end_date"] = end_date
        self.current_family_filter["sort_by"] = sort_by
        self.current_family_filter["order"] = order

        self.handle_load_family_expenses(
            self.current_family_filter["payment_method"],
            self.current_family_filter["shopping_type"],
            self.current_family_filter["category"],
            self.current_family_filter["min_amount"],
            self.current_family_filter["max_amount"],
            self.current_family_filter["start_date"],
            self.current_family_filter["end_date"],
            self.current_family_filter["sort_by"],
            self.current_family_filter["order"]
        )

    def handle_family_previous_page(self):
        if self.family_current_page > 1:
            self.family_current_page -= 1
            if self.current_family_filter:
                self.handle_load_family_expenses(
                    self.current_family_filter["payment_method"],
                    self.current_family_filter["shopping_type"],
                    self.current_family_filter["category"],
                    self.current_family_filter["min_amount"],
                    self.current_family_filter["max_amount"],
                    self.current_family_filter["start_date"],
                    self.current_family_filter["end_date"],
                    self.current_family_filter["sort_by"],
                    self.current_family_filter["order"],
                    current_page=self.family_current_page,
                    page_limit=self.page_limit
                )
            else:
                self.handle_load_family_expenses(
                    current_page=self.family_current_page,
                    page_limit=self.page_limit
                )

    def handle_family_next_page(self):
        if self.family_current_page < self.total_pages:
            self.family_current_page += 1
            if self.current_family_filter:
                self.handle_load_family_expenses(
                    self.current_family_filter["payment_method"],
                    self.current_family_filter["shopping_type"],
                    self.current_family_filter["category"],
                    self.current_family_filter["min_amount"],
                    self.current_family_filter["max_amount"],
                    self.current_family_filter["start_date"],
                    self.current_family_filter["end_date"],
                    self.current_family_filter["sort_by"],
                    self.current_family_filter["order"],
                    current_page=self.family_current_page,
                    page_limit=self.page_limit
                )
            else:
                self.handle_load_family_expenses(
                    current_page=self.family_current_page,
                    page_limit=self.page_limit
                )

    def handle_load_recurring_expense(self,currency_symbol):
        if currency_symbol:
            self.currency_symbol = currency_symbol
        try:
           response = get_family_recurring_expenses(self.get_access_token())["data"]
           self.family_recurring_expense_tab.table_list.setRowCount(len(response))

           for row, each_expense in enumerate(response):
               owner = QTableWidgetItem(each_expense["owner"].title() if each_expense["owner"] else "")
               owner.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
               self.family_recurring_expense_tab.table_list.setItem(row, 0, owner)

               provider_name = QTableWidgetItem(each_expense["provider_name"].title() if each_expense["provider_name"] else "")
               provider_name.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
               self.family_recurring_expense_tab.table_list.setItem(row, 1, provider_name)

               subcategory = QTableWidgetItem(
                   each_expense["subcategory"].title() if each_expense["subcategory"] else "")
               subcategory.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
               self.family_recurring_expense_tab.table_list.setItem(row, 2, subcategory)

               amount = QTableWidgetItem(
                   f"{self.currency_symbol}"+str(each_expense["amount"]).title() if each_expense["amount"] else "")
               amount.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
               self.family_recurring_expense_tab.table_list.setItem(row, 3, amount)

               frequency = QTableWidgetItem(
                   each_expense["frequency"].title() if each_expense["frequency"] else "")
               frequency.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
               self.family_recurring_expense_tab.table_list.setItem(row, 4, frequency)

               notes = QTableWidgetItem(
                   each_expense["notes"].title() if each_expense["notes"] else "")
               notes.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
               self.family_recurring_expense_tab.table_list.setItem(row, 5, notes)


        except requests.ConnectionError:

            connection_error_message_dialog = MessageDialog("Connection Error", "Unable to connect to the server.")

            connection_error_message_dialog.error_dialog()

            connection_error_message_dialog.exec()


        except requests.Timeout:

            timeout_error_message_dialog = MessageDialog("Connection Error", "The request timed out.")

            timeout_error_message_dialog.error_dialog()

            timeout_error_message_dialog.exec()


        except Exception as error:

            if str(error) == "Session Expired":
                self.handle_token_expired()

            api_error_message_dialog = MessageDialog("API Error", str(error))

            api_error_message_dialog.error_dialog()

            api_error_message_dialog.exec()