# src/app.py
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QFrame
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt

from src.widgets.canvas import EditorCanvas


class VectorEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        print("Window Created")

        self.setWindowTitle("Vector Editor")
        self.resize(1000, 700)

        self.current_tool = "line"

        self._init_ui()

    # ================= UI =================

    def _init_ui(self):
        self._create_menu()
        self._create_status_bar()
        self._setup_layout()

    def _create_menu(self):
        file_menu = self.menuBar().addMenu("&File")

        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)

        file_menu.addAction(exit_action)

    def _create_status_bar(self):
        self.statusBar().showMessage("Готов к работе")

    def _setup_layout(self):
        container = QWidget()
        self.setCentralWidget(container)

        main_layout = QHBoxLayout(container)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # ===== Левая панель инструментов =====
        tools_panel = QFrame()
        tools_panel.setFixedWidth(120)
        tools_panel.setFrameShape(QFrame.StyledPanel)

        tools_layout = QVBoxLayout(tools_panel)

        self.btn_line = QPushButton("Line")
        self.btn_rect = QPushButton("Rect")
        self.btn_ellipse = QPushButton("Ellipse")

        for btn in (self.btn_line, self.btn_rect, self.btn_ellipse):
            btn.setCheckable(True)
            tools_layout.addWidget(btn)

        tools_layout.addStretch()

        # по умолчанию
        self.btn_line.setChecked(True)

        # ===== Холст =====
        self.canvas = EditorCanvas()

        # ===== Сигналы =====
        self.btn_line.clicked.connect(lambda: self.on_change_tool("line"))
        self.btn_rect.clicked.connect(lambda: self.on_change_tool("rect"))
        self.btn_ellipse.clicked.connect(lambda: self.on_change_tool("ellipse"))

        # ===== Компоновка =====
        main_layout.addWidget(tools_panel)
        main_layout.addWidget(self.canvas)

    # ================= Logic =================

    def on_change_tool(self, tool_name: str):
        self.current_tool = tool_name
        print(f"Выбран инструмент: {tool_name}")

        self.statusBar().showMessage(f"Инструмент: {tool_name}")

        # поведение RadioButtons
        self.btn_line.setChecked(tool_name == "line")
        self.btn_rect.setChecked(tool_name == "rect")
        self.btn_ellipse.setChecked(tool_name == "ellipse")

        # передаем состояние в Canvas
        self.canvas.set_tool(tool_name)

    # ================= Events =================

    def closeEvent(self, event):
        print("Window Closed")
        event.accept()
