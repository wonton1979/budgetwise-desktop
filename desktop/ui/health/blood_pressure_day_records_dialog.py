from PySide6.QtCore import QTime, Qt
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QWidget

from ui.health.blood_pressure_update_dialog import BloodPressureUpdateDialog
from utils.date_format_convertor import uk_date_format, long_date_format


class BloodPressureDayRecordsDialog(QDialog):
    def __init__(self, handle_edit_health_record, handle_delete_health_record,blood_pressure_day_records,date_format):
        super().__init__()
        self.display_name = None
        self.expense_id = None
        self.date_format = date_format
        self.handle_edit_health_record = handle_edit_health_record
        self.handle_delete_health_record = handle_delete_health_record
        self.setWindowTitle("Blood Pressure Day Records")
        self.setModal(True)
        self.blood_pressure_day_records = blood_pressure_day_records
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(8, 8, 8, 8)
        self.setLayout(self.main_layout)
        self.initialize_information_dialog()

    def initialize_information_dialog(self):

        title_label_layout = QHBoxLayout()
        title_label_layout.setContentsMargins(10,10,10,10)
        title_label_layout.setSpacing(10)
        label_display_date_record = self.blood_pressure_day_records["record_date"]
        match self.date_format:
            case "DD/MM/YYYY":
                label_display_date_record  = uk_date_format(str(self.blood_pressure_day_records["record_date"]))
            case "DD MMM YYYY":
                label_display_date_record = long_date_format(str(self.blood_pressure_day_records["record_date"]))

        message_content_label = QLabel("Blood Pressure and Heart Rate On "+label_display_date_record)
        message_content_label.setStyleSheet("color: #4f46e5;font-size: 12px; font-weight: 600;")

        title_label_layout.addWidget(message_content_label)

        self.main_layout.addLayout(title_label_layout)

        day_records = self.blood_pressure_day_records["records"]

        for record in day_records:
            record["record_date"] = self.blood_pressure_day_records["record_date"]

            reading_layout = QHBoxLayout()
            reading_layout.setContentsMargins(10, 10, 10, 10)
            reading_layout.setSpacing(10)

            record_time = QTime.fromString(record["record_time"],"HH:mm:ss").toString("HH:mm")

            reading_label = QLabel(
                record_time + " : Systolic - " + str(record["systolic_reading"]) + "  Diastolic - " + str(
                    record["diastolic_reading"]) + "  Heart Rate - " + str(record["heart_rate"]))

            container = QWidget()
            container.setStyleSheet("""
                                background: transparent;
                            """)
            button_layout = QHBoxLayout()
            button_layout.setContentsMargins(0, 0, 0, 0)
            button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            update_button = QPushButton("Update")
            update_button.setFixedHeight(28)
            update_button.setFixedWidth(100)
            update_button.setStyleSheet("""
                                                               QPushButton {
                                                                   background-color: #4f46e5;
                                                                   color: white;
                                                                   border-radius: 8px;
                                                                   font-size: 10px;
                                                                   font-weight: 600;
                                                               }
                                                               QPushButton:hover {
                                                                   background-color: #4338ca;
                                                               }
                                                           """)
            update_button.clicked.connect(
                lambda checked=False, payload=record: self.open_update_blood_pressure_record_dialog(payload)
            )

            button_layout.addWidget(update_button)

            container.setLayout(button_layout)

            reading_layout.addWidget(reading_label)
            reading_layout.addWidget(container)

            self.main_layout.addLayout(reading_layout)

        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(10,10,10,15)

        ok_button = QPushButton("OK")
        ok_button.setFixedHeight(28)
        ok_button.setFixedWidth(100)
        ok_button.setStyleSheet("""
                            QPushButton {
                                background-color: #4f46e5;
                                color: white;
                                border-radius: 8px;
                                font-size: 14px;
                                font-weight: 600;
                            }
                            QPushButton:hover {
                                background-color: #4338ca;
                            }
                        """)

        button_layout.addStretch()

        button_layout.addWidget(ok_button)

        button_layout.addStretch()


        self.main_layout.addLayout(button_layout)

        ok_button.clicked.connect(self.reject)

    def open_update_blood_pressure_record_dialog(self, payload):
        self.reject()
        print(self.date_format)
        blood_pressure_update_dialog = BloodPressureUpdateDialog(self.handle_edit_health_record, self.handle_delete_health_record, payload,self.date_format)
        blood_pressure_update_dialog.exec()
