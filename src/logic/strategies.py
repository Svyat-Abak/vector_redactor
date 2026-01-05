import json
from abc import ABC, abstractmethod

from PySide6.QtGui import QImage, QPainter, QColor
from PySide6.QtCore import QRectF


class SaveStrategy(ABC):
    @abstractmethod
    def save(self, filename: str, scene):
        pass


class JsonSaveStrategy(SaveStrategy):
    def save(self, filename, scene):
        data = {
            "version": "1.0",
            "scene": {
                "width": scene.width(),
                "height": scene.height(),
            },
            "shapes": []
        }

        # ВАЖНО: инвертируем порядок для корректного Z-index
        for item in scene.items()[::-1]:
            if hasattr(item, "rect"):
                rect = item.rect()
                data["shapes"].append({
                    "type": "rect",
                    "props": {
                        "x": rect.x(),
                        "y": rect.y(),
                        "w": rect.width(),
                        "h": rect.height(),
                        "color": item.pen().color().name(),
                        "width": item.pen().width(),
                    }
                })

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)


class ImageSaveStrategy(SaveStrategy):
    def __init__(self, fmt="PNG", background="white"):
        self.fmt = fmt
        self.background = background

    def save(self, filename, scene):
        rect = scene.sceneRect()

        image = QImage(
            int(rect.width()),
            int(rect.height()),
            QImage.Format_ARGB32
        )

        if self.background == "transparent":
            image.fill(QColor(0, 0, 0, 0))
        else:
            image.fill(QColor(self.background))

        painter = QPainter(image)
        painter.setRenderHint(QPainter.Antialiasing)
        scene.render(painter, QRectF(image.rect()), rect)
        painter.end()

        image.save(filename, self.fmt)
