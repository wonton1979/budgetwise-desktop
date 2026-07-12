from pathlib import Path

from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout

from ui.components.charts.monthly_category_expense_chart import MonthlyCategoryExpenseChart
from ui.components.charts.monthly_spending_chart import MonthlySpendingChart

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class DashboardPage(QWidget):
    def __init__(self,currency_symbol):
        super().__init__()
        self.currency_symbol = currency_symbol
        self.create_dashboard()

    def create_dashboard(self):
        dashboard_page_layout = QVBoxLayout()
        dashboard_page_layout.setContentsMargins(0, 0, 0, 0)
        dashboard_page_layout.setSpacing(16)
        self.setLayout(dashboard_page_layout)

        self.create_content_area()
        dashboard_page_layout.addWidget(self.content_area, 0)

        self.create_chart_area()
        dashboard_page_layout.addWidget(self.chart_area, 1)

        self.create_bottom_area()
        dashboard_page_layout.addWidget(self.bottom_card, 0)


    def create_content_area(self):
        self.content_area = QFrame()
        self.content_area.setStyleSheet("background: transparent;")
        content_area_layout = QHBoxLayout()
        content_area_layout.setContentsMargins(0, 0, 0, 0)
        content_area_layout.setSpacing(16)
        self.content_area.setLayout(content_area_layout)
        self.content_area.setFixedHeight(120)


        self.expense_card = QFrame()
        self.income_card = QFrame()
        self.recurring_expense_card = QFrame()
        self.balance_card = QFrame()


        for each_card in [self.expense_card, self.income_card, self.recurring_expense_card , self.balance_card]:
            each_card.setStyleSheet("background-color: white; border-radius: 10px;")
            each_card.setFixedHeight(120)
            content_area_layout.addWidget(each_card)

        self.expense_card_value_label = self.setup_metric_card(self.expense_card, "Total Expenses", "£0.00", "credit-card.png")
        self.income_card_value_label = self.setup_metric_card(self.income_card, "Total Income", "£0.00", "pound-sterling.png")
        self.recurring_expense_card_value_label = self.setup_metric_card(self.recurring_expense_card, "Total Recurring Expenses", "£0.00", "recurring.png")
        self.balance_card_value_label = self.setup_metric_card(self.balance_card, "Balance", "£0.00", "wallet.png")


    def create_chart_area(self):
        self.chart_area = QFrame()
        self.chart_area.setStyleSheet("background: transparent;")

        chart_layout = QHBoxLayout()
        chart_layout.setContentsMargins(0, 0, 0, 0)
        chart_layout.setSpacing(16)
        self.chart_area.setLayout(chart_layout)

        spending_chart = QFrame()
        category_chart = QFrame()

        for chart in [spending_chart, category_chart]:
            chart.setStyleSheet("""
                               background-color: white;
                               border-radius: 10px;
                           """)

        chart_layout.addWidget(spending_chart)
        chart_layout.addWidget(category_chart)

        spending_chart.setMinimumHeight(170)
        category_chart.setMinimumHeight(170)

        spending_chart_layout = QVBoxLayout()
        spending_chart.setLayout(spending_chart_layout)

        spending_chart_title = QLabel("Weekly Spending Trend")
        spending_chart_title.setStyleSheet("""
                           font-size: 14px;
                           font-weight: 600;
                           color: #0f172a;
                       """)
        spending_chart_layout.addWidget(spending_chart_title)
        self.monthly_spending_chart = MonthlySpendingChart(self.currency_symbol)


        spending_chart_layout.addWidget(self.monthly_spending_chart)
        spending_chart_layout.addStretch()

        category_chart_layout = QVBoxLayout()
        category_chart.setLayout(category_chart_layout)

        category_chart_title = QLabel("Category Breakdown")
        category_chart_title.setStyleSheet("""
                                   font-size: 14px;
                                   font-weight: 600;
                                   color: #0f172a;
                               """)

        self.category_expenses_chart = MonthlyCategoryExpenseChart()
        category_chart_layout.addWidget(category_chart_title)
        category_chart_layout.addWidget(self.category_expenses_chart)
        category_chart_layout.addStretch()

    def create_bottom_area(self):
        self.bottom_card = QFrame()
        self.bottom_card.setStyleSheet("""
                           background-color: white;
                           border-radius: 12px;
                       """)
        self.bottom_card.setFixedHeight(150)

        bottom_layout = QVBoxLayout()
        self.bottom_card.setLayout(bottom_layout)
        bottom_layout.setContentsMargins(18, 16, 18, 16)

        recent_title = QLabel("Monthly Expenses Summary")
        recent_title.setContentsMargins(0,0,0,20)
        recent_title.setStyleSheet("""
                           color: #0f172a;
                           font-size: 16px;
                           font-weight: 600;
                       """)


        insight_layout = QHBoxLayout()

        label_group_count_layout = QVBoxLayout()
        transaction_count_label = QLabel("Transactions This Month")
        transaction_count_label.setStyleSheet("""
            color: #64748b;
            font-size: 12px;
            font-weight: 500;
        """)

        self.transaction_count_label_value = QLabel("0")
        self.transaction_count_label_value.setStyleSheet("""
            color: #0f172a;
            font-size: 16px;
            font-weight: 700;
        """)

        label_group_top_category_layout = QVBoxLayout()
        top_category_label = QLabel("Top Category")
        top_category_label.setStyleSheet("""
                    color: #64748b;
                    font-size: 12px;
                    font-weight: 500;
                """)

        self.top_category_label_value = QLabel("N/A")
        self.top_category_label_value.setStyleSheet("""
                    color: #0f172a;
                    font-size: 16px;
                    font-weight: 700;
                """)

        label_highest_expense_layout = QVBoxLayout()
        highest_expense_label = QLabel("Highest Expense")
        highest_expense_label.setStyleSheet("""
                            color: #64748b;
                            font-size: 12px;
                            font-weight: 500;
                        """)

        self.highest_expense_label_value = QLabel("0.00")
        self.highest_expense_label_value.setStyleSheet("""
                            color: #0f172a;
                            font-size: 16px;
                            font-weight: 700;
                        """)

        label_average_daily_spending_layout = QVBoxLayout()

        average_daily_spending_label = QLabel("Average Daily Spending")
        average_daily_spending_label.setStyleSheet("""
                                    color: #64748b;
                                    font-size: 12px;
                                    font-weight: 500;
                                """)

        self.average_daily_spending_value = QLabel("0.00")
        self.average_daily_spending_value.setStyleSheet("""
                                    color: #0f172a;
                                    font-size: 16px;
                                    font-weight: 700;
                                """)

        label_group_count_layout.addWidget(transaction_count_label)
        label_group_count_layout.addWidget(self.transaction_count_label_value)

        label_group_top_category_layout.addWidget(top_category_label)
        label_group_top_category_layout.addWidget(self.top_category_label_value)

        label_highest_expense_layout.addWidget(highest_expense_label)
        label_highest_expense_layout.addWidget(self.highest_expense_label_value)

        label_average_daily_spending_layout.addWidget(average_daily_spending_label)
        label_average_daily_spending_layout.addWidget(self.average_daily_spending_value)

        insight_layout.addLayout(label_group_count_layout)
        insight_layout.addLayout(label_group_top_category_layout)
        insight_layout.addLayout(label_highest_expense_layout)
        insight_layout.addLayout(label_average_daily_spending_layout)

        bottom_layout.addWidget(recent_title)
        bottom_layout.addLayout(insight_layout)
        bottom_layout.addStretch()

    def set_button_icon(self, button,icon_name):
        icon_path = BASE_DIR / "icons" / icon_name
        button.setIcon(QIcon(str(icon_path)))
        button.setIconSize(QSize(18, 18))

    def setup_metric_card(self, card, title, value, icon_name):
        card_layout = QVBoxLayout()
        card.setLayout(card_layout)
        card_layout.setContentsMargins(18, 14, 18, 14)

        top_row = QHBoxLayout()

        title_label = QLabel(title)
        title_label.setStyleSheet("""
            color: #64748b;
            font-size: 12px;
        """)

        icon_label = QLabel()
        icon_path = BASE_DIR / "icons" / icon_name
        icon_label.setPixmap(QIcon(str(icon_path)).pixmap(18, 18))

        top_row.addWidget(title_label)
        top_row.addStretch()
        top_row.addWidget(icon_label)

        value_label = QLabel(value)
        value_label.setStyleSheet("""
            color: #0f172a;
            font-size: 26px;
            font-weight: 700;
        """)

        card_layout.addLayout(top_row)
        card_layout.addWidget(value_label)
        card_layout.addStretch()

        return value_label

    def handle_value_update(self,label_widget,value):
        label_widget.setText(value)