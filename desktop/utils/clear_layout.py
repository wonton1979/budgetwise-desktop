def clear_layout(layout):
    while layout.count():
        item = layout.takeAt(0)

        widget = item.widget()
        if widget:
            widget.deleteLater()

        child_layout = item.layout()
        if child_layout:
            clear_layout(child_layout)