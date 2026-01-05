from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QColorDialog


class PropertiesPanel(QWidget):
    def __init__(self, scene, undo_stack):
        super().__init__()
        self.scene = scene

        layout = QVBoxLayout(self)
        btn = QPushButton("Color")
        btn.clicked.connect(self.change_color)
        layout.addWidget(btn)

    def change_color(self):
        color = QColorDialog.getColor()
        if not color.isValid():
            return

        for item in self.scene.selectedItems():
            item.pen().setColor(color)
            item.update()
