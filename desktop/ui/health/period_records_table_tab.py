from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QVBoxLayout, QTableWidget, QHeaderView, QTableWidgetItem

from ui.health.period_record_update_dialog import PeriodUpdateDialog
from utils.date_format_convertor import uk_date_format, long_date_format


class PeriodRecordsTableTab(QFrame):

    def __init__(self, handle_edit_health_record, handle_delete_health_record,date_format):
        super().__init__()
        self.period_record_layout = QVBoxLayout()
        self.period_record_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.period_record_layout)
        self.table_data = None
        self.handle_edit_health_record = handle_edit_health_record
        self.handle_delete_health_record = handle_delete_health_record
        self.date_format = date_format
        self.setStyleSheet("""
            QFrame {
                background-color: white;
            }
        """)
        self.period_records_table = QTableWidget()
        self.create_period_records_table()

    def create_period_records_table(self):

        self.period_records_table.setColumnCount(6)

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

        self.period_record_layout.addWidget(self.period_records_table)


    def load_period_records(self,period_records=None):

        if period_records:
            self.table_data = period_records
            self.period_records_table.setRowCount(len(self.table_data))
            for row,period_record in enumerate(self.table_data):
                self.period_records_table.setItem(row, 0, QTableWidgetItem(str(period_record["health_record_id"])))
                period_month = QTableWidgetItem(period_record["month"])
                period_month.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.period_records_table.setItem(row, 1, period_month)
                period_start_date_display = str(period_record["start_date"])
                match self.date_format:
                    case "DD/MM/YYYY":
                        period_start_date_display = uk_date_format(str(period_record["start_date"]))
                    case "DD MMM YYYY":
                        period_start_date_display = long_date_format(str(period_record["start_date"]))
                start_date = QTableWidgetItem(period_start_date_display)
                start_date.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.period_records_table.setItem(row, 2, start_date)
                period_end_date_display = str(period_record["end_date"])
                match self.date_format:
                    case "DD/MM/YYYY":
                        period_end_date_display = uk_date_format(str(period_record["end_date"]))
                    case "DD MMM YYYY":
                        period_end_date_display = long_date_format(str(period_record["end_date"]))
                end_date = QTableWidgetItem(period_end_date_display)
                end_date.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.period_records_table.setItem(row, 3, end_date)
                duration = QTableWidgetItem(period_record["duration"])
                duration.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.period_records_table.setItem(row, 4, duration)
                notes = QTableWidgetItem(period_record["notes"])
                notes.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.period_records_table.setItem(row, 5, notes)


    def handle_record_cell_clicked(self,row):

        existing_period_record = {
                "health_record_id": self.period_records_table.item(row, 0).text(),
                "start_date": self.period_records_table.item(row, 2).text(),
                "end_date": self.period_records_table.item(row, 3).text(),
                "notes": self.period_records_table.item(row, 5).text()
            }


        self.period_record_update_dialog = PeriodUpdateDialog(self.handle_edit_health_record,
                                                              self.handle_delete_health_record,
                                                              existing_period_record,
                                                              self.date_format)
        self.period_record_update_dialog.exec()

    def update_date_format(self,new_date_format):
        self.date_format =new_date_format
        self.load_period_records()