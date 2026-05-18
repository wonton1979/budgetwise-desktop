from PySide6.QtWidgets import QWidget, QVBoxLayout

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MonthlyCategoryExpenseChart(QWidget):
    def __init__(self):
        super().__init__()

        self.figure = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.figure)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

    def update_chart(self, category_data):

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