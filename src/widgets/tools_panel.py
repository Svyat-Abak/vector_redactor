from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QColorDialog, QLabel
)
from PySide6.QtCore import Qt


class ToolsPanel(QWidget):
    def __init__(self, canvas):
        super().__init__()
        self.canvas = canvas

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)

        # ---------- DRAW TOOLS ----------
        layout.addWidget(QLabel("Draw"))

        self.btn_select = QPushButton("Select")
        self.btn_line = QPushButton("Line")
        self.btn_rect = QPushButton("Rectangle")
        self.btn_ellipse = QPushButton("Ellipse")

        layout.addWidget(self.btn_select)
        layout.addWidget(self.btn_line)
        layout.addWidget(self.btn_rect)
        layout.addWidget(self.btn_ellipse)

        self.btn_select.clicked.connect(lambda: self.canvas.set_tool("select"))
        self.btn_line.clicked.connect(lambda: self.canvas.set_tool("line"))
        self.btn_rect.clicked.connect(lambda: self.canvas.set_tool("rect"))
        self.btn_ellipse.clicked.connect(lambda: self.canvas.set_tool("ellipse"))

        # ---------- EDIT ----------
        layout.addWidget(QLabel("Edit"))

        self.btn_group = QPushButton("Group")
        self.btn_ungroup = QPushButton("Ungroup")
        self.btn_color = QPushButton("Color")
        self.btn_undo = QPushButton("Undo Move")

        layout.addWidget(self.btn_group)
        layout.addWidget(self.btn_ungroup)
        layout.addWidget(self.btn_color)
        layout.addWidget(self.btn_undo)

        self.btn_group.clicked.connect(self.canvas.group_selected_items)
        self.btn_ungroup.clicked.connect(self.canvas.ungroup_selected_items)
        self.btn_undo.clicked.connect(self.canvas.undo_stack.undo)
        self.btn_color.clicked.connect(self.choose_color)

    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.canvas.set_color_for_selected(color)
