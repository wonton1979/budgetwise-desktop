from PySide6.QtCore import QDate
from PySide6.QtWidgets import QFrame, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from ui.health.weight_update_dialog import WeightUpdateDialog


class WeightLineChartTab(QFrame):

    def __init__(self, handle_edit_weight_record, handle_delete_weight_record):
        super().__init__()
        self.weight_record_layout = QVBoxLayout()
        self.weight_record_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.weight_record_layout)
        self.figure = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.figure)
        self.current_hovered_index = None
        self.chart_data = None
        self.weight_record_layout.addWidget(self.canvas)
        self.handle_edit_weight_record = handle_edit_weight_record
        self.handle_delete_weight_record = handle_delete_weight_record

    def create_weight_records_line_chart(self, weight_data):

        self.chart_data = weight_data

        self.figure.clear()

        labels = [
            QDate.fromString(item["record_date"], "dd/MM/yyyy").toString("dd MMM")
            for item in self.chart_data
        ]
        values = [float(item["weight_in_kilograms"]) for item in self.chart_data]

        self.ax = self.figure.add_subplot(111)

        self.ax.plot(labels, values, marker="o",picker=True)
        self.ax.set_ylabel("Weight (Kg)")

        self.canvas.mpl_connect(
            "pick_event",
            self.handle_point_clicked
        )

        self.ax.set_title(
            "Weight Trend\n(Click a point for details)",
            fontsize=10
        )

        self.ax.grid(True, alpha=0.3)
        self.figure.tight_layout()

        self.canvas.draw()

    def handle_point_clicked(self, event):
        index = event.ind[0]
        self.weight_update_dialog =WeightUpdateDialog(self.handle_edit_weight_record, self.handle_delete_weight_record,self.chart_data[index])
        self.weight_update_dialog.exec()








