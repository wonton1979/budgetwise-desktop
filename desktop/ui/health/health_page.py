import requests
from PySide6.QtCore import QDate
from PySide6.QtWidgets import QWidget, QVBoxLayout,QTabWidget, QMessageBox

from services.health_service import get_health_records, add_health_record, update_health_record, delete_health_record
from ui.components.dialogs.message_dialog import MessageDialog
from ui.health.add_health_record import AddHealthRecordFrame
from ui.health.blood_pressure_chart_tab import BloodPressureChartTab
from ui.health.blood_sugar_line_chart_tab import BloodSugarLineChartTab
from ui.health.period_records_table_tab import PeriodRecordsTableTab
from ui.health.weight_line_chart_tab import WeightLineChartTab
from utils.uk_date_format import uk_date_format


class HealthPage(QWidget):
    def __init__(self,access_token_getter,handle_token_expired):
        super().__init__()
        self.get_access_token = access_token_getter
        self.handle_token_expired = handle_token_expired
        self.initialize_health_page_layout()

    def initialize_health_page_layout(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(10)

        self.setLayout(main_layout)

        health_records_tabs = QTabWidget()
        health_records_tabs.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                top: -1px;
            }

            QTabBar::tab {
                background: #1e293b;
                color: #ffffff;
                padding: 8px 16px;
                margin-right: 4px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }

            QTabBar::tab:selected {
                background: #ffffff;
                color: #000000;
                font-weight: 600;
            }

            QTabBar::tab:!selected:hover {
                background: #334155;
                color: #ffffff;
            }
        """)

        self.weight_line_chart = WeightLineChartTab(self.handle_edit_health_record, self.handle_delete_health_record)

        self.blood_pressure_line_chart = BloodPressureChartTab(self.handle_edit_health_record, self.handle_delete_health_record)

        self.blood_sugar_line_chart = BloodSugarLineChartTab(self.handle_edit_health_record, self.handle_delete_health_record)

        self.period_records_table = PeriodRecordsTableTab(self.handle_edit_health_record, self.handle_delete_health_record)

        health_records_tabs.addTab(self.weight_line_chart, "Weight Records Line Chart")
        health_records_tabs.addTab(self.blood_pressure_line_chart, "Blood Pressure Line Chart")
        health_records_tabs.addTab(self.blood_sugar_line_chart, "Blood Sugar Level Line Chart")
        health_records_tabs.addTab(self.period_records_table, "Period Records Table")

        self.add_health_record_frame = AddHealthRecordFrame(self.handle_add_health_record,self.get_access_token)

        main_layout.addWidget(self.add_health_record_frame)
        main_layout.addWidget(health_records_tabs)

    def handle_add_health_record(self,health_record):
        try:
            add_health_record(health_record,self.get_access_token())
            add_weight_success_dialog = MessageDialog(message_title="Information",
                                                      message_content="Health record successfully added!")
            add_weight_success_dialog.information_dialog()
            add_weight_success_dialog.exec()

            self.load_health_records()


        except requests.ConnectionError:

            connection_error_message_dialog = MessageDialog("Connection Error", "Unable to connect to the server.")

            connection_error_message_dialog.error_dialog()

            connection_error_message_dialog.exec()



        except requests.Timeout:

            timeout_error_message_dialog = MessageDialog("Connection Error", "The request timed out.")

            timeout_error_message_dialog.error_dialog()

            timeout_error_message_dialog.exec()



        except Exception as error:

            if str(error) == "Session Expired":
                self.handle_token_expired()

            api_error_message_dialog = MessageDialog("API Error", str(error))

            api_error_message_dialog.error_dialog()

            api_error_message_dialog.exec()

    def load_health_records(self):

        weight_records_for_chart = []
        blood_pressure_records_for_chart = []
        blood_sugar_records_for_chart = []
        period_records_for_table = []

        try:
            response = get_health_records(self.get_access_token())
            weight_records = response["data"]["weight_records"]
            blood_pressure_records = response["data"]["blood_pressure_records"]
            blood_sugar_records = response["data"]["blood_sugar_records"]
            period_records = response["data"]["period_records"]

            for each_record in weight_records:
                weight_records_for_chart.append(
                    {
                        "health_record_id": each_record["health_record_id"],
                        "record_date": uk_date_format(each_record["record_date"]),
                        "weight_in_kilograms": each_record["weight_in_kilograms"],
                        "notes": each_record["notes"],
                    }
                )
            for each_record in blood_pressure_records:
                if  len(blood_pressure_records_for_chart) > 0 and uk_date_format(each_record["record_date"]) == blood_pressure_records_for_chart[-1][
                    "record_date"]:
                    blood_pressure_records_for_chart[-1]["records"].append(
                        {
                            "health_record_id": each_record["health_record_id"],
                            "systolic_reading": each_record["systolic_reading"],
                            "diastolic_reading": each_record["diastolic_reading"],
                            "heart_rate": each_record["heart_rate"],
                            "notes": each_record["notes"],
                            "record_time": each_record["record_time"]
                        }
                    )
                else:
                    blood_pressure_records_for_chart.append(
                        {
                            "record_date": uk_date_format(each_record["record_date"]),
                            "records": [
                                {
                                    "health_record_id": each_record["health_record_id"],
                                    "systolic_reading": each_record["systolic_reading"],
                                    "diastolic_reading": each_record["diastolic_reading"],
                                    "heart_rate": each_record["heart_rate"],
                                    "notes": each_record["notes"],
                                    "record_time": each_record["record_time"]
                                }
                            ]
                        }
                    )

            for each_record in blood_sugar_records:
                if  len(blood_sugar_records_for_chart) > 0 and uk_date_format(each_record["record_date"]) == blood_sugar_records_for_chart[-1][
                    "record_date"]:
                    blood_sugar_records_for_chart[-1]["records"].append(
                        {
                            "health_record_id": each_record["health_record_id"],
                            "blood_sugar_reading": each_record["blood_sugar_reading"],
                            "blood_sugar_reading_type": each_record["blood_sugar_reading_type"],
                            "notes": each_record["notes"],
                            "record_time": each_record["record_time"]
                        }
                    )
                else:
                    blood_sugar_records_for_chart.append(
                        {
                            "record_date": uk_date_format(each_record["record_date"]),
                            "records": [
                                {
                                    "health_record_id": each_record["health_record_id"],
                                    "blood_sugar_reading": each_record["blood_sugar_reading"],
                                    "blood_sugar_reading_type": each_record["blood_sugar_reading_type"],
                                    "notes": each_record["notes"],
                                    "record_time": each_record["record_time"]
                                }
                            ]
                        }
                    )

            for each_record in period_records:
                period_records_for_table.append(
                    {
                        "health_record_id": each_record["health_record_id"],
                        "month": QDate.fromString(each_record["start_date"], "yyyy-MM-dd").toString("MMM yyyy"),
                        "start_date": uk_date_format(each_record["start_date"]),
                        "end_date": uk_date_format(each_record["end_date"]) if each_record["end_date"] else None,
                        "duration": str(QDate.fromString(each_record["start_date"], "yyyy-MM-dd").daysTo(
                            QDate.fromString(each_record["end_date"], "yyyy-MM-dd"))) if each_record[
                            "end_date"] else "Not Set Yet",
                        "notes": each_record["notes"]
                    }
                )

            self.weight_line_chart.create_weight_records_line_chart(weight_records_for_chart)
            self.blood_pressure_line_chart.create_blood_pressure_records_line_chart(blood_pressure_records_for_chart)
            self.blood_sugar_line_chart.create_blood_sugar_records_line_chart(blood_sugar_records_for_chart)
            self.period_records_table.create_period_records_table(period_records_for_table)


        except requests.ConnectionError:

            connection_error_message_dialog = MessageDialog("Connection Error", "Unable to connect to the server.")

            connection_error_message_dialog.error_dialog()

            connection_error_message_dialog.exec()



        except requests.Timeout:

            timeout_error_message_dialog = MessageDialog("Connection Error", "The request timed out.")

            timeout_error_message_dialog.error_dialog()

            timeout_error_message_dialog.exec()



        except Exception as error:

            if str(error) == "Session Expired":
                self.handle_token_expired()

            api_error_message_dialog = MessageDialog("API Error", str(error))

            api_error_message_dialog.error_dialog()

            api_error_message_dialog.exec()

    def handle_edit_health_record(self, health_record_id, updated_health_record):
        try:
            update_health_record(health_record_id,updated_health_record,self.get_access_token())
            self.load_health_records()


        except requests.ConnectionError:

            connection_error_message_dialog = MessageDialog("Connection Error", "Unable to connect to the server.")

            connection_error_message_dialog.error_dialog()

            connection_error_message_dialog.exec()



        except requests.Timeout:

            timeout_error_message_dialog = MessageDialog("Connection Error", "The request timed out.")

            timeout_error_message_dialog.error_dialog()

            timeout_error_message_dialog.exec()



        except Exception as error:

            if str(error) == "Session Expired":
                self.handle_token_expired()

            api_error_message_dialog = MessageDialog("API Error", str(error))

            api_error_message_dialog.error_dialog()

            api_error_message_dialog.exec()


    def handle_delete_health_record(self, health_record_id):
        try:
            delete_health_record(health_record_id,self.get_access_token())
            self.load_health_records()

        except requests.ConnectionError:

            connection_error_message_dialog = MessageDialog("Connection Error", "Unable to connect to the server.")

            connection_error_message_dialog.error_dialog()

            connection_error_message_dialog.exec()


        except requests.Timeout:

            timeout_error_message_dialog = MessageDialog("Connection Error", "The request timed out.")

            timeout_error_message_dialog.error_dialog()

            timeout_error_message_dialog.exec()


        except Exception as error:

            if str(error) == "Session Expired":
                self.handle_token_expired()

            api_error_message_dialog = MessageDialog("API Error", str(error))

            api_error_message_dialog.error_dialog()

            api_error_message_dialog.exec()

    def choose_health_type_to_add(self,health_type):
        self.add_health_record_frame.handle_health_type_changed(health_type)


