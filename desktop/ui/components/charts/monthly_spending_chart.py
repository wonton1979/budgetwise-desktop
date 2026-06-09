from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from utils.clear_layout import clear_layout


class MonthlySpendingChart(QWidget):
    def __init__(self):
        super().__init__()

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.main_layout)

    def update_chart(self, weekly_data):
        if weekly_data[0]["value"] == 0:
            clear_layout(self.main_layout)
            no_data_label = QLabel("📈\n\nNo spending data for this month yet.\n\nAdd your first expense to display the chart.")
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

        labels = [item["label"] for item in weekly_data]
        values = [float(item["value"]) for item in weekly_data]

        ax = self.figure.add_subplot(111)

        ax.plot(labels, values, marker="o")
        ax.set_ylabel("Amount (£)")

        ax.grid(True, alpha=0.3)

        self.figure.tight_layout()
        self.canvas.draw()
