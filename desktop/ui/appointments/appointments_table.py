from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QVBoxLayout, QTableWidget, QHeaderView, QTableWidgetItem

from ui.appointments.appointment_update_dialog import AppointmentUpdateDialog
from utils.date_format_convertor import uk_date_format, long_date_format


class AppointmentTable(QFrame):

    def __init__(self, handle_edit_appointment, handle_delete_appointment,date_format):
        super().__init__()
        self.appointment_update_dialog = None
        self.appointment_list_layout = QVBoxLayout()
        self.appointment_list_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.appointment_list_layout)
        self.table_data = None
        self.handle_edit_appointment = handle_edit_appointment
        self.handle_delete_appointment = handle_delete_appointment
        self.date_format = date_format
        self.setStyleSheet("""
                background-color: white;
        """)
        self.appointment_list_table = QTableWidget()
        self.appointment_list_table.cellDoubleClicked.connect(self.handle_record_cell_clicked)
        self.create_appointment_list_table()

    def create_appointment_list_table(self):
        self.appointment_list_table.setColumnCount(10)

        self.appointment_list_table.setHorizontalHeaderLabels([
            "id", "Date", "Time", "Contact", "Purpose", "Type","Location","Platform","notes","status"
        ])
        self.appointment_list_table.setColumnHidden(0, True)
        self.appointment_list_table.setColumnHidden(8, True)
        self.appointment_list_table.setColumnHidden(9, True)

        self.appointment_list_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.appointment_list_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.appointment_list_table.setAlternatingRowColors(True)


        self.appointment_list_table.setStyleSheet("""
                    QTableWidget {
                        background-color: white;
                        border: none;
                        gridline-color: #e2e8f0;
                        font-size: 13px;
                        margin: 0px;
                        padding: 0px;
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

    def load_appointment_data(self,appointments_data,new_date_format=None):
        if new_date_format:
            self.date_format = new_date_format
        self.appointment_list_table.setRowCount(len(appointments_data))
        for row, appointment in enumerate(appointments_data):
            self.appointment_list_table.setItem(row, 0, QTableWidgetItem(str(appointment["appointment_id"])))
            appointment_date_display = str(appointment["appointment_date"])
            match self.date_format:
                case "DD/MM/YYYY":
                    appointment_date_display = uk_date_format(str(appointment["appointment_date"]))
                case "DD MMM YYYY":
                    appointment_date_display = long_date_format(str(appointment["appointment_date"]))
            appointment_date = QTableWidgetItem(appointment_date_display)
            appointment_date.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.appointment_list_table.setItem(row, 1, appointment_date)
            appointment_time= QTableWidgetItem(appointment["appointment_time"])
            appointment_time.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.appointment_list_table.setItem(row, 2, appointment_time)
            contact = QTableWidgetItem(appointment["contact"].title())
            contact.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.appointment_list_table.setItem(row, 3, contact)
            appointment_purpose = QTableWidgetItem(appointment["appointment_purpose"])
            appointment_purpose.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.appointment_list_table.setItem(row, 4,appointment_purpose)
            appointment_type = QTableWidgetItem(appointment["appointment_type"].title())
            appointment_type.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.appointment_list_table.setItem(row, 5, appointment_type)
            appointment_location = QTableWidgetItem(appointment["appointment_location"])
            appointment_location.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.appointment_list_table.setItem(row, 6, appointment_location)
            online_platform = QTableWidgetItem(appointment["online_platform"])
            online_platform.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.appointment_list_table.setItem(row, 7, online_platform)
            notes = QTableWidgetItem(appointment["notes"])
            notes.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.appointment_list_table.setItem(row, 8, notes)
            status = QTableWidgetItem(appointment["status"].title())
            status.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.appointment_list_table.setItem(row, 9, status)

        self.appointment_list_layout.addWidget(self.appointment_list_table)

    def handle_record_cell_clicked(self, row):
        appointment_id = self.appointment_list_table.item(row, 0)
        appointment_date = self.appointment_list_table.item(row, 1)
        appointment_time = self.appointment_list_table.item(row, 2)
        contact = self.appointment_list_table.item(row, 3)
        appointment_purpose = self.appointment_list_table.item(row, 4)
        appointment_type = self.appointment_list_table.item(row, 5)
        appointment_location = self.appointment_list_table.item(row, 6)
        online_platform = self.appointment_list_table.item(row, 7)
        notes = self.appointment_list_table.item(row, 8)
        status = self.appointment_list_table.item(row, 9)

        if (appointment_id is None or appointment_date is None or appointment_time is None or appointment_type is None
                or appointment_location is None or contact is None or appointment_purpose is None
                or online_platform is None or status is None or notes is None):
            return
        existing_appointment = {
            "id": appointment_id.text(),
            "appointment_date": appointment_date.text(),
            "appointment_time": appointment_time.text(),
            "contact": contact.text(),
            "appointment_purpose": appointment_purpose.text(),
            "appointment_type": appointment_type.text(),
            "appointment_location": appointment_location.text(),
            "online_platform": online_platform.text(),
            "notes": notes.text(),
            "status": status.text()
        }

        self.appointment_update_dialog = AppointmentUpdateDialog(self.handle_edit_appointment,
                                                            self.handle_delete_appointment,
                                                                 existing_appointment,
                                                                 self.date_format
                                                                 )
        self.appointment_update_dialog.exec()