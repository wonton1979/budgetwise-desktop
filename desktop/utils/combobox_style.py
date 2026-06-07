def get_combo_style():
    return """
           QComboBox {
               background-color: #f8fafc;
               border: 1px solid #e2e8f0;
               border-radius: 6px;
               padding: 0 10px;
               font-size: 14px;
           }

           QComboBox QAbstractItemView {
               background-color: white;
               border: 1px solid #e2e8f0;
               selection-background-color: #e2e8f0;
           }
       """