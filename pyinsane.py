import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QSpinBox, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QStackedWidget, QProgressBar
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QMovie
import pyinsane2

class ScanThread(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)
    
    def __init__(self, scanner, dpi, image_name):
        super().__init__()
        self.scanner = scanner
        self.dpi = dpi
        self.image_name = image_name

    def run(self):
        try:
            # Set scanner options
            self.scanner.options['resolution'].value = self.dpi
            self.scanner.options['mode'].value = 'Color'

            # Start scan
            scan_session = self.scanner.scan(multiple=False)
            while True:
                try:
                    scan_session.scan.read()
                except EOFError:
                    break

            # Save the scanned image
            image = scan_session.images[0]
            image.save(f"{self.image_name}.png")
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))

class ScannerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Initialize SANE and get devices
        pyinsane2.init()
        self.devices = pyinsane2.get_devices()

        # UI Elements
        self.setWindowTitle("Scanner Application")

        # Resize application window
        self.resize(300, 200) # w, l

        # Scanner dropdown
        self.scanner_label = QLabel("Select Scanner:")
        self.scanner_dropdown = QComboBox(self)
        for device in self.devices:
            # Use the human-readable model name or a more identifiable part of the device name
            self.scanner_dropdown.addItem(device.model if hasattr(device, 'model') else device.name.split()[-1])

        # DPI option
        self.dpi_label = QLabel("DPI:")
        self.dpi_spinbox = QSpinBox(self)
        self.dpi_spinbox.setRange(50, 1200)  # Adjust DPI range as needed
        self.dpi_spinbox.setValue(300)  # Default DPI value

        # Image name input
        self.image_name_label = QLabel("Image Name:")
        self.image_name_input = QLineEdit(self)
        self.image_name_input.setPlaceholderText("Enter image file name")

        # Scan button
        self.scan_button = QPushButton("Start Scan", self)
        self.scan_button.clicked.connect(self.start_scan)

        # Progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMaximum(0)  # Indeterminate state
        self.progress_bar.setTextVisible(False)

        # Spinner animation
        # self.spinner_label = QLabel(self)
        # self.movie = QMovie("spinner.gif")  # You need a spinner.gif file in the same directory
        # self.spinner_label.setMovie(self.movie)

        # Stack to overlay the progress bar on the scan button
        self.stack = QStackedWidget(self)
        self.stack.addWidget(self.scan_button)
        self.stack.addWidget(self.progress_bar)

        # Layouts
        layout = QVBoxLayout()
        layout.addWidget(self.scanner_label)
        layout.addWidget(self.scanner_dropdown)

        dpi_layout = QHBoxLayout()
        dpi_layout.addWidget(self.dpi_label)
        dpi_layout.addWidget(self.dpi_spinbox)
        layout.addLayout(dpi_layout)

        layout.addWidget(self.image_name_label)
        layout.addWidget(self.image_name_input)
        layout.addWidget(self.stack)
        # layout.addWidget(self.spinner_label)

        self.setLayout(layout)
        self.show()

    def start_scan(self):
        # Get selected scanner and settings
        scanner_name = self.scanner_dropdown.currentText()
        dpi_value = self.dpi_spinbox.value()
        image_name = self.image_name_input.text()

        if not image_name:
            QMessageBox.warning(self, "Error", "Please enter a valid image name.")
            return

        # Find the selected scanner
        selected_scanner = None
        for device in self.devices:
            if (device.model if hasattr(device, 'model') else device.name.split()[-1]) == scanner_name:
                selected_scanner = device
                break

        if selected_scanner:
            try:
                # Disable the scan button and show progress
                self.scan_button.setEnabled(False)
                self.stack.setCurrentWidget(self.progress_bar)  # Show the progress bar
                self.progress_bar.show()
                # self.spinner_label.show()
                # self.movie.start()

                # Start scanning in a separate thread
                self.scan_thread = ScanThread(selected_scanner, dpi_value, image_name)
                self.scan_thread.finished.connect(self.scan_finished)
                self.scan_thread.error.connect(self.scan_error)
                self.scan_thread.start()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred during scanning: {e}")
        else:
            QMessageBox.critical(self, "Error", "Selected scanner not found.")

    def scan_finished(self):
        self.scan_button.setEnabled(True)
        self.stack.setCurrentWidget(self.scan_button)  # Show the scan button again
        self.progress_bar.hide()
        # self.spinner_label.hide()
        # self.movie.stop()
        QMessageBox.information(self, "Success", "Scan completed successfully.")

    def scan_error(self, error_message):
        self.scan_button.setEnabled(True)
        self.stack.setCurrentWidget(self.scan_button)  # Show the scan button again
        self.progress_bar.hide()
        # self.spinner_label.hide()
        # self.movie.stop()
        QMessageBox.critical(self, "Error", f"An error occurred during scanning: {error_message}")

    def closeEvent(self, event):
        # Clean up resources
        pyinsane2.exit()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ScannerApp()
    sys.exit(app.exec_())
