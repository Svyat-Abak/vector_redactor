from PySide6.QtGui import QUndoCommand


class AddCommand(QUndoCommand):
    def __init__(self, scene, item):
        super().__init__("Add")
        self.scene = scene
        self.item = item

    def redo(self):
        self.scene.addItem(self.item)

    def undo(self):
        self.scene.removeItem(self.item)


class MoveCommand(QUndoCommand):
    def __init__(self, item, old_pos, new_pos):
        super().__init__("Move")
        self.item = item
        self.old = old_pos
        self.new = new_pos

    def undo(self):
        self.item.setPos(self.old)

    def redo(self):
        self.item.setPos(self.new)
