from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QDialog, QVBoxLayout

from ui.memorable_days.dialog_content_frame_component import ContentFrameComponent



class UpdateMemorableDayDialog(QDialog):
    def __init__(self, handle_update_memorable_day,handle_delete_memorable_day,existing_memorable_day_data,date_format):
        super().__init__()
        self.savings_id = None
        self.setWindowTitle("Update Memorable Day")
        self.setModal(True)
        self.resize(680, 360)
        self.handle_update_memorable_day = handle_update_memorable_day
        self.handle_delete_memorable_day = handle_delete_memorable_day
        self.existing_memorable_day_data = existing_memorable_day_data
        self.date_format = date_format
        self.create_update_memorable_day_card()


    def create_update_memorable_day_card(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(main_layout)

        update_memorable_day_frame = ContentFrameComponent(
            handle_update_memory_day=self.handle_update_memorable_day_clicked,
            handle_delete_memory_day=self.handle_delete_memorable_day_clicked,
            existing_memorable_day_data=self.existing_memorable_day_data,
            operation="update",
            date_format=self.date_format
        )

        main_layout.addWidget(update_memorable_day_frame)


    def handle_update_memorable_day_clicked(self, new_memorable_day_data,memorable_day_id):

        self.handle_update_memorable_day(new_memorable_day_data,memorable_day_id)
        QTimer.singleShot(2000, self.reject)


    def handle_delete_memorable_day_clicked(self, memorable_day_id):

        self.handle_delete_memorable_day(memorable_day_id)
        QTimer.singleShot(2000, self.reject)