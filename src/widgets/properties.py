from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QSpinBox, QDoubleSpinBox, QPushButton, QColorDialog
)
from PySide6.QtCore import Qt
from src.logic.shapes.shape import Shape
from src.logic.shapes.group import Group

class PropertiesPanel(QWidget):
    def __init__(self, scene):
        super().__init__()
        self.scene = scene
        self._init_ui()
        self.scene.selectionChanged.connect(self.on_selection_changed)

    def _init_ui(self):
        self.setFixedWidth(220)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)

        self.lbl_type = QLabel("Тип: -")
        layout.addWidget(self.lbl_type)

        layout.addWidget(QLabel("Толщина линии"))
        self.spin_width = QSpinBox()
        self.spin_width.setRange(1, 50)
        self.spin_width.valueChanged.connect(self.on_width_changed)
        layout.addWidget(self.spin_width)

        layout.addWidget(QLabel("Цвет"))
        self.btn_color = QPushButton("Выбрать цвет")
        self.btn_color.setFixedHeight(30)
        self.btn_color.clicked.connect(self.on_color_clicked)
        layout.addWidget(self.btn_color)

        geo_layout = QHBoxLayout()
        self.spin_x = QDoubleSpinBox()
        self.spin_x.setRange(-10000, 10000)
        self.spin_x.setPrefix("X: ")
        self.spin_x.valueChanged.connect(self.on_geo_changed)
        geo_layout.addWidget(self.spin_x)

        self.spin_y = QDoubleSpinBox()
        self.spin_y.setRange(-10000, 10000)
        self.spin_y.setPrefix("Y: ")
        self.spin_y.valueChanged.connect(self.on_geo_changed)
        geo_layout.addWidget(self.spin_y)
        layout.addLayout(geo_layout)

        layout.addStretch()
        self.setEnabled(False)

    def on_selection_changed(self):
        selected = self.scene.selectedItems()
        if not selected:
            self.setEnabled(False)
            return

        self.setEnabled(True)
        item = selected[0]

        type_text = getattr(item, "type_name", type(item).__name__)
        if len(selected) > 1:
            type_text += f" (+{len(selected)-1})"
        self.lbl_type.setText(f"Тип: {type_text}")

        width = item.pen().width() if hasattr(item, "pen") and item.pen() else 1
        self.spin_width.blockSignals(True)
        self.spin_width.setValue(width)
        self.spin_width.blockSignals(False)

        color = item.pen().color().name() if hasattr(item, "pen") and item.pen() else "#000000"
        self._set_button_color(color)

        self.spin_x.blockSignals(True)
        self.spin_y.blockSignals(True)
        self.spin_x.setValue(item.x())
        self.spin_y.setValue(item.y())
        self.spin_x.blockSignals(False)
        self.spin_y.blockSignals(False)

    def on_width_changed(self, value):
        for item in self.scene.selectedItems():
            if hasattr(item, "set_stroke_width"):
                item.set_stroke_width(value)
            elif hasattr(item, "pen"):
                pen = item.pen()
                pen.setWidth(value)
                item.setPen(pen)
        self.scene.update()

    def on_color_clicked(self):
        color = QColorDialog.getColor()
        if not color.isValid():
            return
        hex_color = color.name()
        self._set_button_color(hex_color)
        for item in self.scene.selectedItems():
            if hasattr(item, "set_active_color"):
                item.set_active_color(hex_color)
        self.scene.update()

    def on_geo_changed(self, value):
        new_x = self.spin_x.value()
        new_y = self.spin_y.value()
        for item in self.scene.selectedItems():
            item.setPos(new_x, new_y)
        self.scene.update()

    def _set_button_color(self, color: str):
        self.btn_color.setStyleSheet(f"background-color: {color}; border: 1px solid gray;")
