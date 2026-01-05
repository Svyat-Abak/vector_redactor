from PySide6.QtWidgets import (
    QGraphicsView,
    QGraphicsScene,
    QGraphicsItemGroup
)
from PySide6.QtGui import QPainter, QUndoStack
from PySide6.QtCore import Qt

from src.logic.move_command import MoveCommand
from src.logic.tools import SelectionTool, CreationTool
from src.logic.shapes import Shape


class EditorCanvas(QGraphicsView):
    def __init__(self):
        super().__init__()

        # ---------- SCENE ----------
        self.scene = QGraphicsScene(0, 0, 800, 600)
        self.setScene(self.scene)

        # ---------- UNDO ----------
        self.undo_stack = QUndoStack(self)
        self._start_positions = {}

        # ---------- TOOLS ----------
        self.tools = {
            "select": SelectionTool(self),
            "line": CreationTool(self),
            "rect": CreationTool(self),
            "ellipse": CreationTool(self),
        }

        self.current_tool = self.tools["select"]

        # ---------- VIEW ----------
        self.setRenderHint(QPainter.Antialiasing)
        self.setDragMode(QGraphicsView.RubberBandDrag)

    # ---------- TOOL SWITCH ----------

    def set_tool(self, name: str):
        if name not in self.tools:
            return

        tool = self.tools[name]

        # если это инструмент рисования — задаём тип фигуры
        if isinstance(tool, CreationTool):
            tool.shape_type = name

        self.current_tool = tool

    # ---------- GROUPING ----------

    def group_selected_items(self):
        items = self.scene.selectedItems()
        if len(items) < 2:
            return

        group = self.scene.createItemGroup(items)
        group.setFlag(QGraphicsItemGroup.GraphicsItemFlag.ItemIsSelectable, True)
        group.setFlag(QGraphicsItemGroup.GraphicsItemFlag.ItemIsMovable, True)

    def ungroup_selected_items(self):
        for item in self.scene.selectedItems():
            if isinstance(item, QGraphicsItemGroup):
                self.scene.destroyItemGroup(item)

    # ---------- COLOR ----------

    def set_color_for_selected(self, color):
        for item in self.scene.selectedItems():
            if isinstance(item, Shape):
                item.set_active_color(color.name())

    # ---------- UNDO MOVE ----------

    def mousePressEvent(self, event):
        # фиксируем стартовые позиции для undo
        self._start_positions = {
            item: item.pos()
            for item in self.scene.selectedItems()
        }

        if self.current_tool:
            self.current_tool.mouse_press(event)

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.current_tool:
            self.current_tool.mouse_move(event)

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.current_tool:
            self.current_tool.mouse_release(event)

        super().mouseReleaseEvent(event)

        # пушим undo команду
        for item, old_pos in self._start_positions.items():
            new_pos = item.pos()
            if old_pos != new_pos:
                self.undo_stack.push(
                    MoveCommand(item, old_pos, new_pos)
                )
