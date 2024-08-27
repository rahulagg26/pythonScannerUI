# Scanner Application

## Overview

This is a Python-based graphical user interface (GUI) application for scanning documents using available USB scanners. It allows users to select a scanner, set the DPI (dots per inch), and specify a file name for the scanned image. The application provides visual feedback during the scanning process using a progress bar and a spinner animation.

## Features

- **Select Scanner:** Choose from available USB scanners.
- **Set DPI:** Adjust the resolution of the scan.
- **Enter Image Name:** Specify the file name for the scanned image.
- **Progress Indicator:** Shows a loading spinner and progress bar during scanning.
- **Responsive UI:** Uses threading to ensure the GUI remains responsive during the scan.

## Requirements

- Python 3.9.19
- requirements.txt

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/rahulagg26/pythonScannerUI.git
   cd pythonScannerUI
   ```

2. **Install Dependencies:**

   Ensure you have Python 3.9.19 installed. Then, install the required Python packages from requirements.txt

   ```bash
   pip install PyQt5 pyinsane2
   ```

3. **Add Spinner GIF:**

   Download a spinner GIF and place it in the same directory as the script. You can find a simple spinner GIF online or create one yourself.

## Usage

1. **Run the Application:**

   ```bash
   python pyinsane.py
   ```

2. **Using the Application:**

   - **Select Scanner:** Choose your scanner from the dropdown menu.
   - **Set DPI:** Adjust the DPI using the spinner box.
   - **Enter Image Name:** Type the desired file name for the scanned image.
   - **Start Scan:** Click the "Start Scan" button to begin scanning.

   During the scan, a progress bar and spinner animation will indicate that the scan is in progress. Once the scan is complete, the image will be saved with the specified name.

## Code Overview

- **`pyinsane.py`:** The main script for the application. It initializes the GUI, handles user interactions, and manages the scanning process.

- **`ScanThread`:** A `QThread` subclass that performs the scanning operation in a separate thread, keeping the GUI responsive.

## Troubleshooting

- **Scanner Not Detected:** Ensure that the scanner is properly connected and recognized by your system. Check scanner drivers and `pyinsane2` compatibility.

- **No Spinner Animation:** Make sure the `spinner.gif` file is correctly placed in the script directory and is a valid GIF file.

## Contact

For further questions or feedback, please contact [rahulaggarwal1926@gmail.com].
