from PySide6.QtWidgets import (
    QGraphicsPathItem,
    QGraphicsItemGroup
)
from PySide6.QtGui import (
    QPen,
    QColor,
    QPainterPath
)
from PySide6.QtCore import QPointF
from abc import abstractmethod

class Shape(QGraphicsPathItem):
    def __init__(self, color: str = "black", stroke_width: int = 2):
        super().__init__()

        self.color = color
        self.stroke_width = stroke_width

        self._setup_pen()
        self._setup_flags()

    def _setup_pen(self):
        pen = QPen(QColor(self.color))
        pen.setWidth(self.stroke_width)
        self.setPen(pen)
    
    def set_pen_width(self, value: int):
        pen = self.pen()
        pen.setWidth(value)
        self.setPen(pen)

    def set_active_color(self, color: str):
        pen = self.pen()
        pen.setColor(QColor(color))
        self.setPen(pen)

    def _setup_flags(self):
        self.setFlag(QGraphicsPathItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsPathItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsPathItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)


    @property
    @abstractmethod
    def type_name(self) -> str:
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        pass

    @abstractmethod
    def set_geometry(self, start: QPointF, end: QPointF):
        pass

    def set_active_color(self, color: str):
        self.color = color
        pen = self.pen()
        pen.setColor(QColor(color))
        self.setPen(pen)


class Rectangle(Shape):
    def __init__(self, x=0, y=0, w=0, h=0, color="black", stroke_width=2):
        super().__init__(color, stroke_width)
        self.set_geometry(QPointF(x, y), QPointF(x + w, y + h))

    @property
    def type_name(self):
        return "rect"

    def set_geometry(self, start, end):
        x = min(start.x(), end.x())
        y = min(start.y(), end.y())
        w = abs(end.x() - start.x())
        h = abs(end.y() - start.y())

        path = QPainterPath()
        path.addRect(x, y, w, h)
        self.setPath(path)

    def to_dict(self):
        rect = self.path().boundingRect()
        return {
            "type": self.type_name,
            "pos": [self.x(), self.y()],
            "props": {
                "x": rect.x(),
                "y": rect.y(),
                "w": rect.width(),
                "h": rect.height(),
                "color": self.pen().color().name(),
                "stroke_width": self.pen().width()
            }
        }

class Ellipse(Shape):
    @property
    def type_name(self):
        return "ellipse"

    def set_geometry(self, start, end):
        x = min(start.x(), end.x())
        y = min(start.y(), end.y())
        w = abs(end.x() - start.x())
        h = abs(end.y() - start.y())

        path = QPainterPath()
        path.addEllipse(x, y, w, h)
        self.setPath(path)

    def to_dict(self):
        rect = self.path().boundingRect()
        return {
            "type": self.type_name,
            "props": {
                "x": rect.x(),
                "y": rect.y(),
                "w": rect.width(),
                "h": rect.height(),
                "color": self.pen().color().name(),
                "stroke_width": self.pen().width()
            }
        }

class Line(Shape):
    @property
    def type_name(self):
        return "line"

    def set_geometry(self, start, end):
        path = QPainterPath()
        path.moveTo(start)
        path.lineTo(end)
        self.setPath(path)

    def to_dict(self):
        return {
            "type": self.type_name,
            "props": {
                "color": self.pen().color().name(),
                "stroke_width": self.pen().width()
            }
        }

class Group(QGraphicsItemGroup):
    def __init__(self):
        super().__init__()

        self.setFlag(QGraphicsItemGroup.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItemGroup.GraphicsItemFlag.ItemIsMovable, True)
        self.setHandlesChildEvents(True)

    @property
    def type_name(self) -> str:
        return "group"

    def set_pen_width(self, value: int):
        for child in self.childItems():
            if isinstance(child, Shape):
                child.set_pen_width(value)

    def set_active_color(self, color: str):
        for child in self.childItems():
            if isinstance(child, Shape):
                child.set_active_color(color)

    def to_dict(self) -> dict:
        return {
            "type": self.type_name,
            "pos": [self.x(), self.y()],
            "children": [
                child.to_dict()
                for child in self.childItems()
                if hasattr(child, "to_dict")
            ]
        }
