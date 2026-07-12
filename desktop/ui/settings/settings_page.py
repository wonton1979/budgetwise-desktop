from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFrame, QLabel,
    QHBoxLayout, QComboBox
)

from services.user_service import update_user_profile


def create_section_title(text):
    label = QLabel(text)
    label.setStyleSheet("""
        QLabel {
            color: #0f172a;
            font-size: 16px;
            font-weight: 700;
        }
    """)
    return label


def create_divider():
    divider = QFrame()
    divider.setFixedHeight(1)
    divider.setStyleSheet("background-color: #e2e8f0; border: none;")
    return divider


class SettingsPage(QWidget):
    def __init__(self, access_token_getter, handle_token_expired,preferred_currency_display,preferred_date_format):
        super().__init__()
        self.get_access_token = access_token_getter
        self.handle_token_expired = handle_token_expired
        self.preferred_currency_display = preferred_currency_display
        self.preferred_date_format = preferred_date_format
        self.setStyleSheet("background-color: white;")
        self.create_settings_page()


    def create_settings_page(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)

        wrapper = QFrame()
        wrapper.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
            }
        """)

        wrapper_layout = QVBoxLayout()
        wrapper_layout.setContentsMargins(0, 35, 0, 0)
        wrapper_layout.setSpacing(0)
        wrapper.setLayout(wrapper_layout)

        settings_panel = QFrame()
        settings_panel.setFixedWidth(620)
        settings_panel.setObjectName("settingsPanel")
        settings_panel.setStyleSheet("""
            #settingsPanel {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
            }
        """)

        panel_layout = QVBoxLayout()
        panel_layout.setContentsMargins(28, 24, 28, 24)
        panel_layout.setSpacing(22)
        settings_panel.setLayout(panel_layout)

        panel_layout.addWidget(create_section_title("Appearance"), alignment=Qt.AlignmentFlag.AlignCenter)
        panel_layout.addWidget(
            self.create_setting_row(
                "Theme",
                "Choose the visual theme for BudgetWise.",
                [{"text":"System Default (Coming Soon)","value":"default"},
                 {"text":"Light","value":"light"}, {"text":"Dark","value":"dark"}],
                disabled=True
            )
        )

        panel_layout.addWidget(create_divider())

        panel_layout.addWidget(create_section_title("Preferences"), alignment=Qt.AlignmentFlag.AlignCenter)
        currency_type_frame = self.create_setting_row(
                "Currency",
                "Default currency used across the application.",
                [{"text":"GBP (£)","value":"GBP"},
                 {"text":"USD ($)","value":"USD"}, {"text":"EUR (€)","value":"EUR"}],
            combo_value_change_handler=self.combo_value_change_handler,
            preferred_currency=self.preferred_currency_display
            )
        date_format_frame = self.create_setting_row(
                "Date Format",
                "How dates are displayed in tables and forms.",
                [{"text":"DD/MM/YYYY","value":"DD/MM/YYYY"}, {"text":"YYYY-MM-DD","value":"YYYY-MM-DD"},
                 {"text":"DD MMM YYYY","value":"DD MMM YYYY"}],
            combo_value_change_handler=self.combo_value_change_handler,
            preferred_date_format=self.preferred_date_format
            )
        panel_layout.addWidget(currency_type_frame)
        panel_layout.addWidget(date_format_frame)

        panel_layout.addWidget(create_divider())

        panel_layout.addWidget(create_section_title("About"), alignment=Qt.AlignmentFlag.AlignCenter)
        panel_layout.addWidget(self.create_info_row("Application", "BudgetWise Desktop"))
        panel_layout.addWidget(self.create_info_row("Version", "1.0.0"))
        panel_layout.addWidget(self.create_info_row("Built With", "PySide6, FastAPI, SQLAlchemy, SQLite"))

        wrapper_layout.addWidget(settings_panel)
        wrapper_layout.setAlignment(settings_panel, wrapper_layout.alignment())

        center_row = QHBoxLayout()
        center_row.addStretch()
        center_row.addWidget(settings_panel)
        center_row.addStretch()

        wrapper_layout.addLayout(center_row)
        wrapper_layout.addStretch()

        main_layout.addWidget(wrapper)

    def create_setting_row(self, title, description, options,
                           disabled=False,combo_value_change_handler=None,preferred_currency=None,preferred_date_format=None):
        row_frame = QFrame()
        row_frame.setStyleSheet("background-color: transparent; border: none;")

        row_layout = QHBoxLayout()
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(20)
        row_frame.setLayout(row_layout)

        text_column = QVBoxLayout()
        text_column.setSpacing(4)

        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                color: #1e293b;
                font-size: 14px;
                font-weight: 600;
            }
        """)

        description_label = QLabel(description)
        description_label.setWordWrap(True)
        description_label.setStyleSheet("""
            QLabel {
                color: #64748b;
                font-size: 12px;
            }
        """)

        text_column.addWidget(title_label)
        text_column.addWidget(description_label)

        combo = QComboBox()
        for each_option in options:
            combo.addItem(each_option["text"],each_option["value"])
        combo.setFixedWidth(180)
        combo.setFixedHeight(36)
        combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 1px solid #cbd5e1;
                border-radius: 6px;
                padding: 0 10px;
                color: #0f172a;
                font-size: 13px;
            }

            QComboBox:hover {
                border: 1px solid #4f46e5;
            }
        """)

        if preferred_currency:
            currency_index = combo.findData(preferred_currency)
            if currency_index != -1:
                combo.setCurrentIndex(currency_index)

        if preferred_date_format:
            preferred_date_format_index = combo.findData(preferred_date_format)
            if preferred_date_format_index  != -1:
                combo.setCurrentIndex(preferred_date_format_index )


        if combo_value_change_handler:
            combo.currentIndexChanged.connect(lambda :combo_value_change_handler(combo,title))

        if disabled:
            combo.setEnabled(False)
            combo.setToolTip(
                "Theme switching will be available in a future release."
            )
            combo.setFixedWidth(240)

        row_layout.addLayout(text_column)
        row_layout.addStretch()
        row_layout.addWidget(combo)

        return row_frame

    def create_info_row(self, label_text, value_text):
        row_frame = QFrame()
        row_frame.setStyleSheet("background-color: transparent; border: none;")

        row_layout = QHBoxLayout()
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_frame.setLayout(row_layout)

        label = QLabel(label_text)
        label.setStyleSheet("""
            QLabel {
                color: #64748b;
                font-size: 13px;
                font-weight: 500;
            }
        """)

        value = QLabel(value_text)
        value.setStyleSheet("""
            QLabel {
                color: #1e293b;
                font-size: 13px;
                font-weight: 600;
            }
        """)

        row_layout.addWidget(label)
        row_layout.addStretch()
        row_layout.addWidget(value)

        return row_frame

    def combo_value_change_handler(self,combobox,title):

        if title == "Currency":
            update_user_profile({"preferred_currency_display":combobox.currentData()},self.get_access_token())
        if title == "Date Format":
            update_user_profile({"preferred_date_format": combobox.currentData()}, self.get_access_token())

