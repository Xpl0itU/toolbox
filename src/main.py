import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QTextEdit,
    QComboBox,
    QFrame,
)
from MergePDFsUtility import MergePDFsUtility
from SplitAudioUtility import SplitAudioUtility
from OrganizeFilesUtility import OrganizeFilesUtility
from ScreenshotsToDocumentUtility import ScreenshotsToDocumentUtility


class Xpl0itUToolbox(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Xpl0itU's Toolbox")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.utility_selector = QComboBox()
        self.utility_selector.addItem("Select Utility")
        self.utility_selector.addItem("Split Audio")
        self.utility_selector.addItem("Merge PDFs")
        self.utility_selector.addItem("Organize Files")
        self.utility_selector.addItem("Screenshots to Document")
        self.utility_selector.currentIndexChanged.connect(self.show_parameters)
        layout.addWidget(self.utility_selector)

        self.parameter_frame = QFrame()
        self.parameter_layout = QVBoxLayout(self.parameter_frame)
        layout.addWidget(self.parameter_frame)

        self.log_widget = QTextEdit()
        self.log_widget.setReadOnly(True)
        layout.addWidget(self.log_widget)

        run_button = QPushButton("Run")
        run_button.clicked.connect(self.run_selected_utility)
        layout.addWidget(run_button)

        self.utilities = {
            "Split Audio": SplitAudioUtility("Split Audio"),
            "Organize Files": OrganizeFilesUtility("Organize Files"),
            "Merge PDFs": MergePDFsUtility("Merge PDFs"),
            "Screenshots to Document": ScreenshotsToDocumentUtility(
                "Screenshots to document"
            ),
        }

        self.current_utility = None

    def clear_layout(self, layout):
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
                layout.removeItem(layout.itemAt(i))

    def show_parameters(self, index):
        self.clear_layout(self.parameter_layout)

        selected_utility_name = self.utility_selector.currentText()

        if selected_utility_name == "Select Utility":
            self.current_utility = None
            return

        self.current_utility = self.utilities[selected_utility_name]
        self.current_utility.create_parameter_widgets()

        for widget in self.current_utility.parameter_widgets:
            self.parameter_layout.addWidget(widget)

    def run_selected_utility(self):
        self.log_widget.clear()

        if self.current_utility is None:
            self.log_widget.append("Select a utility to run.")
            return

        result = self.current_utility.run()

        self.log_widget.append(result)


def main():
    app = QApplication(sys.argv)
    window = Xpl0itUToolbox()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
