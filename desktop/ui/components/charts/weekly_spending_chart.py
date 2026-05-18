from PySide6.QtWidgets import QWidget, QVBoxLayout

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class WeeklySpendingChart(QWidget):
    def __init__(self):
        super().__init__()

        self.figure = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.figure)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

    def update_chart(self, weekly_data):
        self.figure.clear()

        labels = [item["label"] for item in weekly_data]
        values = [float(item["value"]) for item in weekly_data]

        ax = self.figure.add_subplot(111)

        ax.plot(labels, values, marker="o")
        ax.set_ylabel("Amount (£)")

        ax.grid(True, alpha=0.3)

        self.figure.tight_layout()
        self.canvas.draw()