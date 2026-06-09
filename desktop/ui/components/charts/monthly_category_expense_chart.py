from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from utils.clear_layout import clear_layout


class MonthlyCategoryExpenseChart(QWidget):
    def __init__(self):
        super().__init__()

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.main_layout)

    def update_chart(self, category_data):

        if not category_data:
            clear_layout(self.main_layout)
            no_data_label = QLabel("📊\n\nNo spending data for this month yet.\n\nAdd your first expense to display the chart.")
            no_data_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_data_label.setStyleSheet("""
                    QLabel {
                        color: #777;
                        font-size: 15px;
                        padding: 40px;
                    }
                """)
            self.main_layout.addSpacing(70)
            self.main_layout.addWidget(no_data_label)

            return

        clear_layout(self.main_layout)
        self.figure = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.figure)

        self.main_layout.addWidget(self.canvas)

        self.figure.clear()

        labels = [item["category"].title() for item in category_data]
        values = [float(item["amount"]) for item in category_data]

        ax = self.figure.add_subplot(111)

        ax.pie(
            values,
            labels=labels,
            autopct="%1.2f%%"
        )

        self.figure.tight_layout()
        self.canvas.draw()