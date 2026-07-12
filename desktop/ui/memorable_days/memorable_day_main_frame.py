from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor, QIcon
from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QWidget, QHBoxLayout

from ui.memorable_days.add_memorable_day_dialog import AddMemorableDayDialog
from ui.memorable_days.update_memorable_day_dialog import UpdateMemorableDayDialog
from utils.clickable_frame import ClickableFrame
from utils.date_format_convertor import uk_date_format, long_date_format

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class MemorableDaysFrame(QFrame):

    def __init__(self,handle_add_memorable_day,handle_update_memorable_day,handle_delete_memorable_day,date_format):
        super().__init__()
        self.handle_add_memorable_day = handle_add_memorable_day
        self.handle_update_memorable_day = handle_update_memorable_day
        self.handle_delete_memorable_day = handle_delete_memorable_day
        self.date_format = date_format
        self.memorable_day_frame_layout = QVBoxLayout()
        self.memorable_day_frame_layout.setContentsMargins(10, 10, 10, 10)
        self.setStyleSheet("""
                        background-color: white;
                        border-radius: 10px;
                   """)
        self.setLayout(self.memorable_day_frame_layout)
        self.memorable_days_cards_container()

    def memorable_days_cards_container(self):

        self.memorable_cards_row_one_layout = QHBoxLayout()
        self.memorable_cards_row_one_layout.setContentsMargins(10, 10, 0, 0)
        self.memorable_cards_row_one_layout.setSpacing(8)

        self.memorable_cards_row_two_layout= QHBoxLayout()
        self.memorable_cards_row_two_layout.setContentsMargins(10, 10, 0, 0)
        self.memorable_cards_row_two_layout.setSpacing(8)

        self.memorable_cards_row_three_layout = QHBoxLayout()
        self.memorable_cards_row_three_layout.setContentsMargins(10, 10, 0, 0)
        self.memorable_cards_row_three_layout.setSpacing(8)

        self.memorable_day_frame_layout.addLayout(self.memorable_cards_row_one_layout)
        self.memorable_day_frame_layout.addLayout(self.memorable_cards_row_two_layout)
        self.memorable_day_frame_layout.addLayout(self.memorable_cards_row_three_layout)
        self.memorable_day_frame_layout.addStretch()


    def add_memorable_day_card(self):

        empty_card_box_frame = ClickableFrame()
        empty_card_box_frame.setStyleSheet("""
            ClickableFrame {
                background-color: white;
                border: 1px solid #4f46e5;
                border-radius: 6px;
            }

            ClickableFrame:hover {
                border: 2px solid #3b82f6;
            }
        """)
        empty_card_box_frame.setFixedHeight(180)
        empty_card_box_frame.setFixedWidth(225)
        empty_card_box_frame.setCursor(QCursor(Qt.CursorShape.OpenHandCursor))
        empty_card_box_frame.clicked.connect(self.add_memorable_day_clicked)

        card_box_frame_layout = QVBoxLayout()
        card_box_frame_layout.setContentsMargins(10, 10, 10, 10)
        card_box_frame_layout.setSpacing(20)

        empty_card_box_frame.setLayout(card_box_frame_layout)

        plus_icon_label = QLabel()
        icon_path = BASE_DIR / "icons" / "plus.png"
        plus_icon_label.setPixmap(QIcon(str(icon_path)).pixmap(38, 38))

        text_label = QLabel("Add New Memorable Day")
        text_label.setStyleSheet("""
                            font-size: 14px;
                            color: #64748b;
                        """)

        card_box_frame_layout.addStretch()
        card_box_frame_layout.addWidget(
            plus_icon_label,
            alignment=Qt.AlignmentFlag.AlignCenter
        )
        card_box_frame_layout.addWidget(text_label, alignment=Qt.AlignmentFlag.AlignCenter)
        card_box_frame_layout.addStretch()

        return empty_card_box_frame

    def create_memorable_day_details_card(self, memorable_day_data,new_date_format=None):
        if new_date_format:
            self.date_format = new_date_format
        if memorable_day_data:

            card_box_frame = ClickableFrame()
            card_box_frame.setObjectName("savingsCard")

            card_box_frame.setStyleSheet("""
                        QFrame#savingsCard {
                            background-color: white;
                            border: 1px solid #4f46e5;
                            border-radius: 6px;
                        }
                        QFrame#savingsCard:hover {
                            background-color: #eff6ff;
                            border: 2px solid #3b82f6;
                        }
                    """)
            card_box_frame.setFixedHeight(180)
            card_box_frame.setFixedWidth(225)
            card_box_frame.setCursor(QCursor(Qt.CursorShape.OpenHandCursor))
            card_box_frame.clicked.connect(lambda clicked=False, existing_memorable_day_data = memorable_day_data :  self.handle_updated_button_clicked(existing_memorable_day_data))

            card_box_frame_layout = QVBoxLayout()
            card_box_frame_layout.setContentsMargins(0, 10, 0, 10)
            card_box_frame_layout.setSpacing(0)

            card_box_frame.setLayout(card_box_frame_layout)

            event_name_label = QLabel(f"{memorable_day_data["event_name"].title()}")
            event_name_label.setStyleSheet("""   
                                                background-color: transparent;
                                                color: #334155;
                                                font-size: 12px;
                                                font-weight: 700;
                                            """)

            event_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            separate_line = QFrame()
            separate_line.setFixedHeight(1)
            separate_line.setStyleSheet("""
                           background-color: #4f46e5;
                           border: none;
                       """)
            separate_line.setContentsMargins(0, 0, 0, 0)

            card_box_frame_layout.addWidget(event_name_label)
            card_box_frame_layout.addSpacing(5)
            card_box_frame_layout.addWidget(separate_line)

            details_container = QWidget()
            details_layout = QVBoxLayout()
            details_container.setLayout(details_layout)
            details_container.setStyleSheet("""
                                   background-color: transparent;;
                                   border: none;
                               """)

            row_layout = QVBoxLayout()
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setSpacing(15)

            memorable_day_type = memorable_day_data["memorable_day_type"].title()
            memorable_day_date = memorable_day_data["memorable_date"]
            match self.date_format:
                case "DD/MM/YYYY":
                    memorable_day_date = uk_date_format(str(memorable_day_data["memorable_date"]))
                case "DD MMM YYYY":
                    memorable_day_date = long_date_format(str(memorable_day_data["memorable_date"]))
            remaining_days = memorable_day_data["days_remaining"]

            memorable_day_label = QLabel(f"Type: {memorable_day_type}")
            memorable_day_label.setStyleSheet("""
                                                                       color: #334155;
                                                                       font-size: 12px;
                                                                       font-weight: 700;
                                                                   """)

            memorable_day_date_label = QLabel(f"Born:  {memorable_day_date}")
            memorable_day_date_label.setStyleSheet("""
                                                                                   color: #334155;
                                                                                   font-size: 12px;
                                                                                   font-weight: 700;
                                                                               """)

            remaining_days_label = QLabel(f"Remaining Days: {remaining_days}")
            remaining_days_label.setStyleSheet("""
                                                                                               color: #334155;
                                                                                               font-size: 12px;
                                                                                               font-weight: 700;
                                                                                           """)



            row_layout.addWidget(memorable_day_label)
            row_layout.addWidget(memorable_day_date_label)
            row_layout.addWidget(remaining_days_label)
            row_layout.addSpacing(5)

            details_layout.addLayout(row_layout)
            details_layout.addStretch()
            card_box_frame_layout.addWidget(details_container)

        else:
            card_box_frame = QFrame()

            card_box_frame.setStyleSheet("""
                                    QFrame#savingsCard {
                                        background-color: white;
                                    }
                                """)
            card_box_frame.setFixedHeight(180)
            card_box_frame.setFixedWidth(225)

            card_box_frame_layout = QVBoxLayout()
            card_box_frame_layout.setContentsMargins(0, 10, 0, 10)
            card_box_frame_layout.setSpacing(0)

            card_box_frame.setLayout(card_box_frame_layout)

        return card_box_frame


    def add_memorable_day_clicked(self):
        self.add_memorable_day_dialog = AddMemorableDayDialog(self.handle_add_memorable_day,self.date_format)
        self.add_memorable_day_dialog.exec_()


    def handle_updated_button_clicked(self,memorable_day_data):
        self.update_memorable_day_dialog = UpdateMemorableDayDialog(self.handle_update_memorable_day,
                                                                    self.handle_delete_memorable_day,
                                                                    memorable_day_data,self.date_format
                                                                    )
        self.update_memorable_day_dialog.exec_()