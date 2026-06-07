from PySide6.QtWidgets import QFrame, QVBoxLayout, QStackedWidget

from ui.health.blood_pressure_form import BloodPressureForm
from ui.health.blood_sugar_form import BloodSugarForm
from ui.health.period_form import PeriodForm
from ui.health.weight_form import WeightForm


class AddHealthRecordFrame(QFrame):
    def __init__(self,handle_add_health_record,access_token_getter):
        super().__init__()
        self.handle_add_health_record = handle_add_health_record
        self.initialize_widgets()
        self.get_access_token = access_token_getter

    def initialize_widgets(self):
        self.setStyleSheet("""
                    background-color: white;
                    border-radius: 10px;
                """)
        self.setFixedHeight(250)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(4)
        self.setLayout(main_layout)

        self.health_form_stack = QStackedWidget()
        self.add_weight_record_form = WeightForm(self.handle_add_health_record)
        self.add_blood_pressure_record_form = BloodPressureForm(self.handle_add_health_record)
        self.add_blood_sugar_record_form = BloodSugarForm(self.handle_add_health_record)
        self.period_record_form = PeriodForm(self.handle_add_health_record)
        self.health_form_stack.addWidget(self.add_weight_record_form)
        self.health_form_stack.addWidget(self.add_blood_pressure_record_form)
        self.health_form_stack.addWidget(self.add_blood_sugar_record_form)
        self.health_form_stack.addWidget(self.period_record_form)
        self.health_form_stack.setCurrentWidget(self.add_weight_record_form)

        main_layout.addWidget(self.health_form_stack)
        main_layout.addStretch()

    def handle_health_type_changed(self,health_type):

        match health_type:
            case "weight record": self.health_form_stack.setCurrentWidget(self.add_weight_record_form)
            case "blood pressure record": self.health_form_stack.setCurrentWidget(self.add_blood_pressure_record_form)
            case "blood sugar record": self.health_form_stack.setCurrentWidget(self.add_blood_sugar_record_form)
            case "period record": self.health_form_stack.setCurrentWidget(self.period_record_form)





