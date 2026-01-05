from PySide6.QtCore import QPointF
from src.logic.factory import ShapeFactory

class SelectionTool:
    def __init__(self, canvas):
        self.canvas = canvas

    def mousePressEvent(self, event): pass
    def mouseMoveEvent(self, event): pass
    def mouseReleaseEvent(self, event): pass


class CreationTool:
    def __init__(self, canvas):
        self.canvas = canvas
        self.shape_type = "rect"
        self.start = None
        self.temp_item = None

    def set_shape(self, shape_type: str):
        self.shape_type = shape_type

    def mousePressEvent(self, event):
        self.start = self.canvas.mapToScene(event.pos())
        self.temp_item = ShapeFactory.create(
            self.shape_type,
            self.start,
            self.start
        )
        if self.temp_item:
            self.canvas.scene.addItem(self.temp_item)

    def mouseMoveEvent(self, event):
        if not self.temp_item:
            return
        end = self.canvas.mapToScene(event.pos())
        self.canvas.scene.removeItem(self.temp_item)
        self.temp_item = ShapeFactory.create(
            self.shape_type,
            self.start,
            end
        )
        self.canvas.scene.addItem(self.temp_item)

    def mouseReleaseEvent(self, event):
        self.temp_item = None
