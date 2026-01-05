from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from src.widgets.canvas import EditorCanvas
from src.widgets.tools_panel import ToolsPanel


class VectorEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Vector Editor")
        self.resize(1100, 700)

        self.canvas = EditorCanvas()
        self.tools = ToolsPanel(self.canvas)

        central = QWidget()
        layout = QHBoxLayout(central)

        layout.addWidget(self.tools)
        layout.addWidget(self.canvas, 1)

        self.setCentralWidget(central)
