import requests
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFrame, QLabel,
    QPushButton, QHBoxLayout, QTreeWidget, QHeaderView, QTreeWidgetItem,QAbstractItemView
)

from services.recurring_expense_service import add_recurring_expense, get_recurring_expense, update_recurring_expense, \
    delete_recurring_expense
from ui.components.dialogs.message_dialog import MessageDialog
from ui.recurring_expenses.add_recurring_expense_dialog import AddRecurringExpenseDialog
from ui.recurring_expenses.edit_recurring_expense_dialog import EditRecurringExpenseDialog


class RecurringExpensePage(QWidget):
    def __init__(self,access_token_getter,handle_token_expired,currency_symbol,date_format):
        super().__init__()
        self.get_access_token = access_token_getter
        self.handle_token_expired = handle_token_expired
        self.currency_symbol = currency_symbol
        self.date_format = date_format
        self.create_recurring_expense_page()


    def create_recurring_expense_page(self):

        recurring_expense_page_layout = QVBoxLayout()
        recurring_expense_page_layout.setContentsMargins(0, 0, 0, 0)
        recurring_expense_page_layout.setSpacing(16)
        self.setLayout(recurring_expense_page_layout)

        self.add_recurring_expense_dialog = AddRecurringExpenseDialog(self.handle_add_expense,self.date_format)
        self.create_tree_card()

        recurring_expense_page_layout.addWidget(self.tree_card)


    def create_tree_card(self):
        self.tree_card = QFrame()
        self.tree_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
            }
        """)

        self.tree_layout = QVBoxLayout()
        self.tree_layout.setContentsMargins(18, 16, 18, 16)
        self.tree_card.setLayout(self.tree_layout)

        self.recurring_tree = QTreeWidget()
        self.recurring_tree.setColumnCount(6)
        self.recurring_tree.setHeaderLabels([
            "Category / Bill",
            "Provider Name",
            "Amount",
            "Frequency",
            "Payment Method",
            "Action"
        ])

        self.recurring_tree.headerItem().setTextAlignment(
            5,
            Qt.AlignmentFlag.AlignCenter
        )

        self.recurring_tree.setRootIsDecorated(True)
        self.recurring_tree.setAlternatingRowColors(True)
        self.recurring_tree.setIndentation(24)
        self.recurring_tree.setExpandsOnDoubleClick(True)
        self.recurring_tree.setEditTriggers(QTreeWidget.EditTrigger.NoEditTriggers)

        self.recurring_tree.setSelectionMode(
            QAbstractItemView.SelectionMode.NoSelection
        )

        self.recurring_tree.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.recurring_tree.header().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.recurring_tree.header().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.recurring_tree.header().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.recurring_tree.header().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)

        self.recurring_tree.setStyleSheet("""
            QTreeWidget {
                background-color: white;
                border: none;
                font-size: 13px;
                color: #0f172a;
            }

            QTreeWidget::item {
                height: 34px;
                padding: 4px;
            }
            
            QTreeWidget::item:hover {
                background-color: #cfe0ff;
                color: #111827;
            }
            
            QHeaderView::section {
                background-color: #f8fafc;
                color: #475569;
                font-size: 13px;
                font-weight: 600;
                padding: 8px;
                border: none;
                border-bottom: 1px solid #e2e8f0;
            }
        """)

        self.recurring_tree.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.no_record_found_info_label = QLabel("")

        self.no_record_found_info_label.setStyleSheet("color: #4f46e5;font-size: 12px; font-weight: 600;")

        self.tree_layout.addWidget(self.recurring_tree)
        self.tree_layout.addWidget(self.no_record_found_info_label)

    def populate_tree(self,currency_symbol):

        self.recurring_tree.clear()
        self.currency_symbol = currency_symbol
        category_list = ["Housing","Utilities","Insurance","Subscription","Healthcare","Transport","Other"]
        try:

            response =get_recurring_expense(self.get_access_token())

            for each_category in response["data"]:
                if each_category["category"].title() in category_list:
                    category_list.remove(each_category["category"].title())
                each_category_top_level = QTreeWidgetItem(
                    [
                        each_category["category"].title() + f" ( {self.currency_symbol}{str(each_category["total_amount"])} )",
                        ""
                        "",
                        "",
                        ""
                    ]
                )
                for each_child_expense in each_category["expenses"]:
                    each_expense = QTreeWidgetItem([
                        each_child_expense["subcategory"].title(),
                        each_child_expense["provider_name"].title(),
                        "£"+str(each_child_expense["amount"]),
                        each_child_expense["frequency"].title(),
                        each_child_expense["payment_method"].title(),
                        ""
                    ])
                    each_expense.setTextAlignment(1, Qt.AlignmentFlag.AlignCenter)
                    each_expense.setTextAlignment(2, Qt.AlignmentFlag.AlignCenter)
                    each_expense.setTextAlignment(3, Qt.AlignmentFlag.AlignCenter)
                    each_expense.setTextAlignment(4, Qt.AlignmentFlag.AlignCenter)

                    each_category_top_level.addChild(each_expense)

                    container = QWidget()
                    container.setStyleSheet("""
                        background: transparent;
                    """)
                    button_layout = QHBoxLayout()
                    button_layout.setContentsMargins(0, 0, 0, 0)
                    button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)



                    self.recurring_tree.setItemWidget(each_expense, 5, container)
                    update_button = QPushButton("Update")
                    update_button.setFixedHeight(28)
                    update_button.setFixedWidth(100)
                    update_button.setStyleSheet("""
                                                       QPushButton {
                                                           background-color: #4f46e5;
                                                           color: white;
                                                           border-radius: 8px;
                                                           font-size: 10px;
                                                           font-weight: 600;
                                                       }
                                                       QPushButton:hover {
                                                           background-color: #4338ca;
                                                       }
                                                   """)
                    button_layout.addWidget(update_button)

                    container.setLayout(button_layout)

                    expense = each_child_expense
                    expense["category"] = each_category["category"]

                    update_button.clicked.connect(
                        lambda checked=False, payload=expense: self.open_update_recurring_expense_dialog(payload)
                    )

                    self.recurring_tree.setItemWidget(each_expense, 5, container)

                self.recurring_tree.addTopLevelItem(each_category_top_level)

            for each_category in category_list:
                each_category_top_level = QTreeWidgetItem(
                    [
                        each_category.title() + f" ( {self.currency_symbol}{str(0.00)} )",
                        ""
                        "",
                        "",
                        ""
                    ]
                )
                self.recurring_tree.addTopLevelItem(each_category_top_level)

        except requests.ConnectionError:

            connection_error_message_dialog = MessageDialog("Connection Error", "Unable to connect to the server.")

            connection_error_message_dialog.error_dialog()

            connection_error_message_dialog.exec()


        except requests.Timeout:

            timeout_error_message_dialog = MessageDialog("Connection Error", "The request timed out.")

            timeout_error_message_dialog.error_dialog()

            timeout_error_message_dialog.exec()


        except Exception as error:

            if str(error) == "Expense not found or not belongs to this user":
                self.no_record_found_info_label.setText("No recurring expenses yet. Add your first recurring expense to get started.")
                for each_category in ["Housing","Utilities","Insurance","Subscription","Healthcare","Transport","Other"]:
                    each_category_top_level = QTreeWidgetItem(
                        [
                            each_category.title() + f" ( {self.currency_symbol}{str(0.00)} )",
                            ""
                            "",
                            "",
                            ""
                        ]
                    )
                    self.recurring_tree.addTopLevelItem(each_category_top_level)
                return

            if str(error) == "Session Expired":
                self.handle_token_expired()
                return

            api_error_message_dialog = MessageDialog("API Error", str(error))

            api_error_message_dialog.error_dialog()

            api_error_message_dialog.exec()


    def handle_add_expense(self,recurring_expense_data):

        try:
            add_recurring_expense(recurring_expense_data, self.get_access_token())
            self.populate_tree(self.currency_symbol)
            self.add_recurring_expense_dialog.add_recurring_expense_notify_label.setText("Add new recurring expense successfully.")
            QTimer.singleShot(2000, self.add_recurring_expense_dialog.reject)

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

    def open_update_recurring_expense_dialog(self,expense):

        self.update_recurring_expense_dialog = EditRecurringExpenseDialog(
            handle_edit_expense=self.handle_update_recurring_expense,
            handle_delete_expense=self.handle_delete_recurring_expense,
            existing_payload=expense,
            date_format=self.date_format,
        )

        self.update_recurring_expense_dialog.exec()

    def handle_update_recurring_expense(self,expense_id,expenses_data):

        try:
            response = update_recurring_expense(expense_id,expenses_data, self.get_access_token())
            if response:
                self.populate_tree(self.currency_symbol)


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

    def handle_delete_recurring_expense(self,expense_id):

        try:

            response = delete_recurring_expense(expense_id, self.get_access_token())
            if response:
                self.populate_tree(self.currency_symbol)

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

    def update_date_format(self,new_date_format):
        self.date_format = new_date_format






