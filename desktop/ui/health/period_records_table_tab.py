from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QVBoxLayout, QTableWidget, QHeaderView, QTableWidgetItem

from ui.health.period_record_update_dialog import PeriodUpdateDialog
from utils.clear_layout import clear_layout


class PeriodRecordsTableTab(QFrame):

    def __init__(self, handle_edit_health_record, handle_delete_health_record):
        super().__init__()
        self.period_record_layout = QVBoxLayout()
        self.period_record_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.period_record_layout)
        self.chart_data = None
        self.period_records_table = None
        self.handle_edit_health_record = handle_edit_health_record
        self.handle_delete_health_record = handle_delete_health_record
        self.setStyleSheet("""
            QFrame {
                background-color: white;
            }
        """)
        self.period_records_table = QTableWidget()

    def create_period_records_table(self,period_records):

        self.period_records_table.setColumnCount(6)
        self.period_records_table.setRowCount(len(period_records))
        self.period_records_table.setHorizontalHeaderLabels([
                "id", "Month", "Start Date", "End Date", "Duration (Days)","Notes"
            ])
        self.period_records_table.setColumnHidden(0, True)

        self.period_records_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.period_records_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.period_records_table.setAlternatingRowColors(True)
        self.period_records_table.cellDoubleClicked.connect(self.handle_record_cell_clicked)

        self.period_records_table.setStyleSheet("""
                    QTableWidget {
                        background-color: white;
                        border: none;
                        gridline-color: #e2e8f0;
                        font-size: 13px;
                    }

                    QHeaderView::section {
                        background-color: #e2e8f0;
                        color: #0f172a;
                        font-weight: 600;
                        padding: 10px;
                        border: none;
                        border-bottom: 1px solid #cbd5e1;
                    }

                    QTableCornerButton::section {
                        background-color: #e2e8f0;
                        border: none;
                        border-bottom: 1px solid #cbd5e1;
                    }
                    
                """)

        for row,period_record in enumerate(period_records):
            self.period_records_table.setItem(row, 0, QTableWidgetItem(str(period_record["health_record_id"])))
            period_month = QTableWidgetItem(period_record["month"])
            period_month.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.period_records_table.setItem(row, 1, period_month)
            start_date = QTableWidgetItem(period_record["start_date"])
            start_date.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.period_records_table.setItem(row, 2, start_date)
            end_date = QTableWidgetItem(period_record["end_date"])
            end_date.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.period_records_table.setItem(row, 3, end_date)
            duration = QTableWidgetItem(period_record["duration"])
            duration.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.period_records_table.setItem(row, 4, duration)
            notes = QTableWidgetItem(period_record["notes"])
            notes.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.period_records_table.setItem(row, 5, notes)

        self.period_record_layout.addWidget(self.period_records_table)

    def handle_record_cell_clicked(self,row):

        existing_period_record = {
                "health_record_id": self.period_records_table.item(row, 0).text(),
                "start_date": self.period_records_table.item(row, 2).text(),
                "end_date": self.period_records_table.item(row, 3).text(),
                "notes": self.period_records_table.item(row, 5).text()
            }

        self.period_record_update_dialog = PeriodUpdateDialog(self.handle_edit_health_record, self.handle_delete_health_record, existing_period_record)
        self.period_record_update_dialog.exec()