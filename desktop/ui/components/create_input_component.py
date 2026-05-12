from PySide6.QtWidgets import QLabel, QLineEdit


class CreateInputComponent:
    def __init__(self,parent_layout, label_text, placeholder_text, text_value=None, readonly=False):
        self.parent_layout = parent_layout
        self.label_text = label_text
        self.placeholder_text = placeholder_text
        self.text_value = text_value
        self.readonly = readonly
        self.create_input_group()

    def create_input_group(self):
        label = QLabel(self.label_text)
        label.setStyleSheet("""
               color: #334155;
               font-size: 13px;
               font-weight: 500;
           """)

        self.input_field = QLineEdit()
        if self.text_value:
            self.input_field.setText(self.text_value)
        else:
            self.input_field.setPlaceholderText(self.placeholder_text)
        self.input_field.setReadOnly(self.readonly)
        self.input_field.setFixedHeight(38)

        if self.readonly:
            self.input_field.setStyleSheet("""
                   QLineEdit {
                       background-color: #f1f5f9;
                       color: #64748b;
                       border: 1px solid #e2e8f0;
                       border-radius: 8px;
                       padding: 0 10px;
                       font-size: 14px;
                   }
               """)
        else:
            self.input_field.setStyleSheet("""
                   QLineEdit {
                       background-color: #f8fafc;
                       color: #0f172a;
                       border: 1px solid #e2e8f0;
                       border-radius: 8px;
                       padding: 0 10px;
                       font-size: 14px;
                   }

                   QLineEdit:focus {
                       border: 1px solid #4f46e5;
                   }
               """)

        self.parent_layout.addWidget(label)
        self.parent_layout.addWidget(self.input_field)

        return self.input_field

    def get_input_text(self):
        return self.input_field.text()