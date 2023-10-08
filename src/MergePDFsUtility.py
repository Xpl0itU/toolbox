from PySide6.QtWidgets import (
    QPushButton,
    QFileDialog,
    QGroupBox,
    QFormLayout,
    QLabel,
    QLineEdit,
)
from Utility import Utility
import pypdf


def merge_pdfs(output_file, input_files):
    pdf_merger = pypdf.PdfMerger()

    for input_file in input_files:
        try:
            pdf_merger.append(input_file)
        except pypdf.utils.PdfReadError:
            print(f"Error loading file: {input_file}")

    with open(output_file, "wb") as output_pdf:
        pdf_merger.write(output_pdf)

    return f"PDF files merged successfully! Output file: {output_file}"


class MergePDFsUtility(Utility):
    def create_parameter_widgets(self):
        group_box = QGroupBox("Merge PDFs Parameters")
        layout = QFormLayout()

        self.pdf_output_file_label = QLabel("Output PDF File:")
        self.pdf_output_file_edit = QLineEdit()
        self.pdf_output_file_edit.setReadOnly(True)
        self.pdf_output_file_button = QPushButton("Select Output PDF File")
        self.pdf_output_file_button.clicked.connect(self.select_output_pdf_file)

        self.pdf_input_files_label = QLabel("Input PDF Files:")
        self.pdf_input_files_edit = QLineEdit()
        self.pdf_input_files_edit.setReadOnly(True)
        self.pdf_input_files_button = QPushButton("Select Input PDF Files")
        self.pdf_input_files_button.clicked.connect(self.select_input_pdf_files)

        layout.addRow(self.pdf_output_file_label, self.pdf_output_file_edit)
        layout.addRow(self.pdf_output_file_button)
        layout.addRow(self.pdf_input_files_label, self.pdf_input_files_edit)
        layout.addRow(self.pdf_input_files_button)

        group_box.setLayout(layout)
        self.parameter_widgets = [group_box]

    def get_parameters(self):
        return {
            "output_file": self.pdf_output_file_edit.text(),
            "input_files": self.pdf_input_files_edit.text().split(","),
        }

    def run(self):
        output_file = self.get_parameters()["output_file"]
        input_files = self.get_parameters()["input_files"]
        return merge_pdfs(output_file, input_files)

    def select_output_pdf_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getSaveFileName(
            self.pdf_output_file_button,
            "Select Output PDF File",
            "",
            "PDF Files (*.pdf);;All Files (*)",
            options=options,
        )
        if file_path:
            self.pdf_output_file_edit.setText(file_path)

    def select_input_pdf_files(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_paths, _ = QFileDialog.getOpenFileNames(
            self.pdf_input_files_button,
            "Select Input PDF Files",
            "",
            "PDF Files (*.pdf);;All Files (*)",
            options=options,
        )
        if file_paths:
            self.pdf_input_files_edit.setText(",".join(file_paths))
