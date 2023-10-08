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
import subprocess
from datetime import datetime


def split_audio(input_file, time_file, output_folder) -> str:
    os.makedirs(output_folder, exist_ok=True)

    with open(time_file, "r") as file:
        time_entries = [
            line.strip().split(" ")
            for line in file
            if line.strip() and not line.startswith("#")
        ]

    for index, entry in enumerate(time_entries):
        start_time = datetime.strptime(entry[0], "%H:%M:%S")
        end_time = (
            datetime.strptime(time_entries[index + 1][0], "%H:%M:%S")
            if index < len(time_entries) - 1
            else None
        )
        name = entry[1]

        command = [
            "ffmpeg",
            "-i",
            input_file,
            "-ss",
            start_time.strftime("%H:%M:%S"),
        ]

        if end_time:
            command.extend(["-to", end_time.strftime("%H:%M:%S")])

        command.append(os.path.join(output_folder, f"{name}.mp3"))

        return str(subprocess.run(command).stdout)


class SplitAudioUtility(Utility):
    def create_parameter_widgets(self):
        group_box = QGroupBox("Split Audio Parameters")
        layout = QFormLayout()

        self.output_directory_label = QLabel("Output Directory:")
        self.output_directory_line_edit = QLineEdit()
        self.output_directory_line_edit.setReadOnly(True)
        self.output_directory_button = QPushButton("Select Output Directory")
        self.output_directory_button.clicked.connect(self.select_output_directory)

        self.audio_input_file_label = QLabel("Input Audio File:")
        self.audio_input_file_edit = QLineEdit()
        self.audio_input_file_edit.setReadOnly(True)
        self.audio_input_file_button = QPushButton("Select Audio File")
        self.audio_input_file_button.clicked.connect(self.select_audio_file)

        self.timestamps_file_label = QLabel("Timestamps File:")
        self.timestamps_file_edit = QLineEdit()
        self.timestamps_file_edit.setReadOnly(True)
        self.timestamps_file_button = QPushButton("Select Timestamps File")
        self.timestamps_file_button.clicked.connect(self.select_timestamps_file)

        layout.addRow(self.output_directory_label, self.output_directory_line_edit)
        layout.addRow(self.output_directory_button)
        layout.addRow(self.audio_input_file_label, self.audio_input_file_edit)
        layout.addRow(self.audio_input_file_button)
        layout.addRow(self.timestamps_file_label, self.timestamps_file_edit)
        layout.addRow(self.timestamps_file_button)

        group_box.setLayout(layout)
        self.parameter_widgets = [group_box]

    def get_parameters(self):
        return {
            "output_directory": self.output_directory_line_edit.text(),
            "input_file": self.audio_input_file_edit.text(),
            "timestamps_file": self.timestamps_file_edit.text(),
        }

    def run(self):
        output_directory = self.get_parameters()["output_directory"]
        input_file = self.get_parameters()["input_file"]
        timestamps_file = self.get_parameters()["timestamps_file"]
        return split_audio(input_file, timestamps_file, output_directory)

    def select_audio_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(
            self.audio_input_file_button,
            "Select Audio File",
            "",
            "All Files (*)",
            options=options,
        )
        if file_path:
            self.audio_input_file_edit.setText(file_path)

    def select_timestamps_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(
            self.timestamps_file_button,
            "Select Timestamps File",
            "",
            "All Files (*)",
            options=options,
        )
        if file_path:
            self.timestamps_file_edit.setText(file_path)

    def select_output_directory(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path = QFileDialog.getExistingDirectory(
            self.output_directory_button,
            "Select Output Directory",
            "",
            options=options,
        )
        if file_path:
            self.output_directory_line_edit.setText(file_path)
