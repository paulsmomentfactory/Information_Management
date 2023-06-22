import os
import tempfile
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel

class DirectoryCopyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Directory Structure Copy'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        layout = QVBoxLayout()
        self.source_dir_button = QPushButton('Select Source Directory', self)
        self.target_dir_button = QPushButton('Select Target Directory', self)
        self.copy_button = QPushButton('Copy Directory Structure', self)
        self.copy_button.setStyleSheet('background-color: green; color: white;')
        self.status_label = QLabel('', self)
        layout.addWidget(self.source_dir_button)
        layout.addWidget(self.target_dir_button)
        layout.addWidget(self.copy_button)
        layout.addWidget(self.status_label)
        self.setLayout(layout)
        self.source_dir_button.clicked.connect(self.select_source_directory)
        self.target_dir_button.clicked.connect(self.select_target_directory)
        self.copy_button.clicked.connect(self.copy_directory_structure)

    def select_source_directory(self):
        self.source_dir = QFileDialog.getExistingDirectory(self, "Select Source Directory")
        self.status_label.setText(f'Source Directory Selected: {self.source_dir}')

    def select_target_directory(self):
        self.target_dir = QFileDialog.getExistingDirectory(self, "Select Target Directory")
        self.status_label.setText(f'Target Directory Selected: {self.target_dir}')

    def has_write_permissions(self, directory):
        try:
            tempfile.TemporaryFile(dir=directory).close()
        except OSError:
            return False
        return True

    def get_all_paths(self, directory):
        paths = []
        for dirpath, _, _ in os.walk(directory):
            paths.append(dirpath)
        return paths

    def copy_directory_structure(self):
        if not hasattr(self, 'source_dir') or not hasattr(self, 'target_dir'):
            self.status_label.setText('Please select both source and target directories.')
            return
        if not self.has_write_permissions(self.target_dir):
            self.status_label.setText(f"Write permissions are required for the directory {self.target_dir}.")
            return
        paths = self.get_all_paths(self.source_dir)
        for path in paths:
            relative_path = os.path.relpath(path, self.source_dir)
            new_path = os.path.join(self.target_dir, relative_path)
            os.makedirs(new_path, exist_ok=True)
        self.status_label.setText('Directory structure successfully copied.')

def main():
    app = QApplication([])
    ex = DirectoryCopyApp()
    ex.show()
    app.exec_()

if __name__ == '__main__':
    main()
