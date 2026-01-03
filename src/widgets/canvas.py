from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtCore import Qt

from src.logic.tools import SelectionTool, CreationTool
from src.logic.shapes import Group


class EditorCanvas(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setSceneRect(0, 0, 800, 600)

        self.setMouseTracking(True)

        self.tools = {
            "select": SelectionTool(self),
            "rect": CreationTool(self, "rect"),
            "ellipse": CreationTool(self, "ellipse"),
            "line": CreationTool(self, "line"),
        }

        self.current_tool = self.tools["select"]

    def set_tool(self, tool_name):
        if tool_name in self.tools:
            self.current_tool = self.tools[tool_name]

            if tool_name == "select":
                self.setCursor(Qt.ArrowCursor)
            else:
                self.setCursor(Qt.CrossCursor)


    def mousePressEvent(self, event):
        self.current_tool.mouse_press(event)

    def mouseMoveEvent(self, event):
        self.current_tool.mouse_move(event)

    def mouseReleaseEvent(self, event):
        self.current_tool.mouse_release(event)


    def group_selected_items(self):
        selected = self.scene.selectedItems()
        if len(selected) < 2:
            return

        group = Group()
        self.scene.addItem(group)

        for item in selected:
            item.setSelected(False)
            group.addToGroup(item)

        group.setSelected(True)

    def ungroup_selected_items(self):
        for item in self.scene.selectedItems():
            if isinstance(item, Group):
                self.scene.destroyGroup(item)
    
    def group_selection(self):
        selected_items = self.scene.selectedItems()
        if len(selected_items) < 2:
            return

        group = Group()
        self.scene.addItem(group)

        for item in selected_items:
            item.setSelected(False)
            group.addToGroup(item)

        group.setSelected(True)

    def ungroup_selection(self):
        for item in self.scene.selectedItems():
            if isinstance(item, Group):
                self.scene.destroyGroup(item)
