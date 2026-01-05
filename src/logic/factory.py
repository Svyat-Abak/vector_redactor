from PySide6.QtWidgets import (
    QGraphicsRectItem,
    QGraphicsEllipseItem,
    QGraphicsLineItem
)
from PySide6.QtGui import QPen, QBrush
from PySide6.QtCore import Qt, QRectF, QPointF

class ShapeFactory:
    @staticmethod
    def create(shape_type: str, start: QPointF, end: QPointF):
        pen = QPen(Qt.black, 2)
        brush = QBrush(Qt.lightGray)

        if shape_type == "rect":
            item = QGraphicsRectItem(QRectF(start, end).normalized())
            item.setBrush(brush)

        elif shape_type == "ellipse":
            item = QGraphicsEllipseItem(QRectF(start, end).normalized())
            item.setBrush(brush)

        elif shape_type == "line":
            item = QGraphicsLineItem(start.x(), start.y(), end.x(), end.y())

        else:
            return None

        item.setPen(pen)
        item.setFlags(
            item.GraphicsItemFlag.ItemIsSelectable |
            item.GraphicsItemFlag.ItemIsMovable
        )
        return item
