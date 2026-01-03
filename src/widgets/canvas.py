from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtCore import Qt

from src.logic.tools import SelectionTool, CreationTool


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
