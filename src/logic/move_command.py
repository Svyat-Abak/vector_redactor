
from PySide6.QtGui import QUndoCommand


class MoveCommand(QUndoCommand):
    def __init__(self, item, old_pos, new_pos):
        super().__init__("Move")
        self.item = item
        self.old_pos = old_pos
        self.new_pos = new_pos

    def undo(self):
        self.item.setPos(self.old_pos)

    def redo(self):
        self.item.setPos(self.new_pos)
