import os
import tempfile
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QLineEdit, QInputDialog

# THIS CONTAINS TEMPLATE CREATIONG AND SAVING.
class DirectoryTemplateApp(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Directory Structure Template'
        self.templates = {}
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        layout = QVBoxLayout()
        self.source_dir_button = QPushButton('Select Source Directory', self)
        self.template_name_input = QLineEdit(self)
        self.template_name_input.setPlaceholderText("Enter template name")
        self.save_template_button = QPushButton('Save Directory Structure as Template', self)
        self.apply_template_button = QPushButton('Apply Template to Directory', self)
        self.apply_template_button.setStyleSheet('background-color: green; color: white;')
        self.status_label = QLabel('', self)
        layout.addWidget(self.source_dir_button)
        layout.addWidget(self.template_name_input)
        layout.addWidget(self.save_template_button)
        layout.addWidget(self.apply_template_button)
        layout.addWidget(self.status_label)
        self.setLayout(layout)
        self.source_dir_button.clicked.connect(self.select_source_directory)
        self.save_template_button.clicked.connect(self.save_directory_structure)
        self.apply_template_button.clicked.connect(self.apply_directory_structure)

    def select_source_directory(self):
        self.source_dir = QFileDialog.getExistingDirectory(self, "Select Source Directory")
        self.status_label.setText(f'Source Directory Selected: {self.source_dir}')

    def get_all_paths(self, directory):
        paths = []
        for dirpath, _, _ in os.walk(directory):
            paths.append(os.path.relpath(dirpath, directory))
        return paths

    def save_directory_structure(self):
        if not hasattr(self, 'source_dir'):
            self.status_label.setText('Please select a source directory.')
            return
        template_name = self.template_name_input.text()
        if not template_name:
            self.status_label.setText('Please enter a template name.')
            return
        self.templates[template_name] = self.get_all_paths(self.source_dir)
        self.status_label.setText(f'Directory structure saved as template: {template_name}')

    def apply_directory_structure(self):
        if not self.templates:
            self.status_label.setText('No templates saved.')
            return
        template_name, okPressed = QInputDialog.getItem(self, "Select Template","Template:", list(self.templates.keys()), 0, False)
        if okPressed and template_name:
            target_dir = QFileDialog.getExistingDirectory(self, "Select Target Directory")
            if target_dir:
                target_dir = os.path.join(target_dir, os.path.basename(self.source_dir))  # this line was added
                for relative_path in self.templates[template_name]:
                    new_path = os.path.join(target_dir, relative_path)
                    os.makedirs(new_path, exist_ok=True)
                self.status_label.setText(f'Applied template {template_name} to {target_dir}')

def main():
    app = QApplication([])
    ex = DirectoryTemplateApp()
    ex.show()
    app.exec_()

if __name__ == '__main__':
    main()
