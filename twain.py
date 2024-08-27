import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QSpinBox, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
import pyinsane2

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

        # Scanner dropdown
        self.scanner_label = QLabel("Select Scanner:")
        self.scanner_dropdown = QComboBox(self)
        for device in self.devices:
            self.scanner_dropdown.addItem(device.name)

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
        layout.addWidget(self.scan_button)

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
            if device.name == scanner_name:
                selected_scanner = device
                break

        if selected_scanner:
            try:
                # Set scanner options
                selected_scanner.options['resolution'].value = dpi_value
                selected_scanner.options['mode'].value = 'Color'

                # Start scan
                scan_session = selected_scanner.scan(multiple=False)
                while True:
                    try:
                        scan_session.scan.read()
                    except EOFError:
                        break

                # Save the scanned image
                image = scan_session.images[0]
                image.save(f"{image_name}.png")
                QMessageBox.information(self, "Success", f"Scan completed and saved as {image_name}.png")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred during scanning: {e}")
        else:
            QMessageBox.critical(self, "Error", "Selected scanner not found.")

    def closeEvent(self, event):
        # Clean up resources
        pyinsane2.exit()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ScannerApp()
    sys.exit(app.exec_())


# import pyinsane2

# # Initialize SANE
# pyinsane2.init()

# try:
#     # Get available devices (scanners)
#     devices = pyinsane2.get_devices()
#     if not devices:
#         print("No scanners found.")
#         exit(1)
    
#     # Select the first available scanner
#     scanner = devices[0]
#     print(f"Using scanner: {scanner.name}")

#     # Set scanner options (e.g., resolution, scan area)
#     scanner.options['resolution'].value = 300  # Set resolution to 300 DPI
#     scanner.options['mode'].value = 'Color'    # Set scan mode to Color
    
#     # Start the scan
#     scan_session = scanner.scan(multiple=False)
    
#     # Retrieve scanned image
#     while True:
#         try:
#             scan_session.scan.read()
#         except EOFError:
#             break
    
#     # The image is now available
#     image = scan_session.images[0]
    
#     # Save the scanned image to a file
#     image.save("scanned_image.png")
#     print("Scan completed and saved as scanned_image.png")

# finally:
#     # Always close the SANE interface to clean up resources
#     pyinsane2.exit()
