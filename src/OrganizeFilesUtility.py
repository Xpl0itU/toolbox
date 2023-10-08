from PySide6.QtWidgets import (
    QPushButton,
    QFileDialog,
    QGroupBox,
    QFormLayout,
    QLabel,
    QLineEdit,
)
from Utility import Utility
import os
import shutil


def organize_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            source_file_path = os.path.join(root, file)
            extension = os.path.splitext(file)[1].lower()
            if extension:
                # Construct the destination folder path while preserving the original folder structure
                if os.path.exists(os.path.join(folder_path, extension[1:])):
                    destination_file_path = os.path.join(
                        folder_path,
                        extension[1:],
                        os.path.relpath(root, source_file_path),
                    )
                    if os.path.exists(destination_file_path):
                        continue
                relative_path = os.path.relpath(root, folder_path)
                destination_folder = os.path.join(
                    folder_path, extension[1:], relative_path
                )
                os.makedirs(destination_folder, exist_ok=True)
                destination_file_path = os.path.join(destination_folder, file)

                # Check if the file already exists in the destination folder
                if not os.path.exists(destination_file_path):
                    shutil.move(source_file_path, destination_file_path)


class OrganizeFilesUtility(Utility):
    def create_parameter_widgets(self):
        group_box = QGroupBox("Organize Files Parameters")
        layout = QFormLayout()

        self.input_directory_label = QLabel("Input Directory:")
        self.input_directory_line_edit = QLineEdit()
        self.input_directory_line_edit.setReadOnly(True)
        self.input_directory_button = QPushButton("Select Input Directory")
        self.input_directory_button.clicked.connect(self.select_input_directory)

        layout.addRow(self.input_directory_label, self.input_directory_line_edit)
        layout.addRow(self.input_directory_button)

        group_box.setLayout(layout)
        self.parameter_widgets = [group_box]

    def get_parameters(self):
        return {
            "input_directory": self.input_directory_line_edit.text(),
        }

    def run(self):
        input_directory = self.get_parameters()["input_directory"]
        return organize_folder(input_directory)

    def select_input_directory(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path = QFileDialog.getExistingDirectory(
            self.input_directory_button,
            "Select Input Directory",
            "",
            options=options,
        )
        if file_path:
            self.input_directory_line_edit.setText(file_path)
