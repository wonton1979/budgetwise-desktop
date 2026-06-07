from PySide6.QtCore import QDate
from PySide6.QtWidgets import QFrame, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from ui.health.blood_pressure_day_records_dialog import BloodPressureDayRecordsDialog


class BloodPressureChartTab(QFrame):

    def __init__(self, handle_edit_health_record, handle_delete_health_record):
        super().__init__()
        self.blood_pressure_record_layout = QVBoxLayout()
        self.blood_pressure_record_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.blood_pressure_record_layout)
        self.figure = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.figure)
        self.current_hovered_index = None
        self.chart_data = None
        self.blood_pressure_record_layout.addWidget(self.canvas)
        self.handle_edit_health_record = handle_edit_health_record
        self.handle_delete_health_record = handle_delete_health_record

    def create_blood_pressure_records_line_chart(self, blood_pressure_data):

        self.chart_data = blood_pressure_data

        self.figure.clear()

        self.labels = [
            QDate.fromString(item["record_date"], "dd/MM/yyyy").toString("dd MMM")
            for item in self.chart_data
        ]

        systolic_values = [int(item["records"][0]["systolic_reading"]) for item in self.chart_data]

        diastolic_values = [int(item["records"][0]["diastolic_reading"]) for item in self.chart_data]

        self.ax = self.figure.add_subplot(111)

        self.ax.plot(self.labels, systolic_values, marker="o",picker=True,label="Systolic")
        self.ax.plot(self.labels, diastolic_values, marker="o", picker=True, label="Diastolic")

        self.ax.set_ylabel("Blood Pressure (mmHg)")

        self.canvas.mpl_connect(
            "pick_event",
            self.handle_point_clicked
        )

        self.ax.set_title(
            "Blood Pressure Trend\n(Click a point for details)",
            fontsize=10
        )

        self.ax.grid(True, alpha=0.3)
        self.figure.tight_layout()
        self.ax.legend()
        self.canvas.draw()

    def handle_point_clicked(self, event):
        index = event.ind[0]
        blood_pressure_data_for_the_date = None
        for each_date_records in self.chart_data:
            if self.labels[index] == QDate.fromString(each_date_records["record_date"], "dd/MM/yyyy").toString("dd MMM"):
                blood_pressure_data_for_the_date = each_date_records
        self.blood_pressure_day_records_dialog =BloodPressureDayRecordsDialog(self.handle_edit_health_record, self.handle_delete_health_record,blood_pressure_data_for_the_date)
        self.blood_pressure_day_records_dialog.exec_()