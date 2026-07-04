def get_date_picker_style():
    return """
        QCalendarWidget {
            background-color: white;
        }

        QCalendarWidget QToolButton {
            color: #333;
            background-color: white;
            font-weight: bold;
            font-size: 14px;
            border: none;
        }

        QCalendarWidget QToolButton:hover {
            color: #333;
            background-color: #eef2ff;
            border-radius: 4px;
        }

        QCalendarWidget QMenu {
            background-color: white;
            color: #333;
        }

        QCalendarWidget QMenu::item {
            background-color: white;
            color: #333;
            padding: 6px 20px;
        }

        QCalendarWidget QMenu::item:selected {
            background-color: #eef2ff;
            color: #333;
        }

        QCalendarWidget QAbstractItemView {
            color: #222;
            selection-background-color: #4f46e5;
            selection-color: white;
        }
    """