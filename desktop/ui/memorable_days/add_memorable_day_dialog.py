from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QDialog, QVBoxLayout

from ui.memorable_days.dialog_content_frame_component import ContentFrameComponent



class AddMemorableDayDialog(QDialog):
    def __init__(self, handle_add_memorable_day):
        super().__init__()
        self.savings_id = None
        self.setWindowTitle("Add New Memorable Day")
        self.setModal(True)
        self.resize(680, 360)
        self.handle_add_memorable_day = handle_add_memorable_day

        self.create_add_memorable_day_card()


    def create_add_memorable_day_card(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(main_layout)

        add_memorable_day_frame = ContentFrameComponent(handle_add_memorable_day = self.handle_add_memorable_day_clicked,operation="add")

        main_layout.addWidget(add_memorable_day_frame)


    def handle_add_memorable_day_clicked(self,new_memorable_day_data):

        self.handle_add_memorable_day(new_memorable_day_data)
        QTimer.singleShot(2000, self.reject)


