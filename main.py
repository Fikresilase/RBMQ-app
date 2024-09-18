import sys
import numpy as np
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QFileDialog,
    QLabel,
    QRadioButton,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QSizePolicy,
    QMessageBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PIL import Image

# Define the quantization median values for each group (32 groups with a width of 8)
median_values = [4, 12, 20, 28, 36, 44, 52, 60, 68, 76, 84, 92, 100, 108, 116, 124,
                 132, 140, 148, 156, 164, 172, 180, 188, 196, 204, 212, 220, 228, 236, 244, 252]

def apply_median_quantization(img_array):
    """Apply median quantization to the image."""
    quantized_array = np.zeros_like(img_array)
    
    for i, median in enumerate(median_values):
        lower_bound = i * 8
        upper_bound = lower_bound + 7
        quantized_array[(img_array >= lower_bound) & (img_array <= upper_bound)] = median
    
    return quantized_array

def apply_bit_reduction(img_array):
    """Reduce bit depth from 8 bits to 5 bits (32 levels)."""
    reduced_bit_image = np.right_shift(img_array, 3)  # Bit reduction
    return reduced_bit_image

class ImageProcessor(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Image Processing App')
        self.setGeometry(100, 100, 800, 600)
        
        # Apply dark theme (optional)
        # Uncomment the following lines to use a dark theme:
        # import qdarkstyle
        # self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Main layout (vertical)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Top section with instruction and choose image button
        self.top_section = QHBoxLayout()
        self.layout.addLayout(self.top_section)

        self.label_instruction = QLabel('1. Select an image', self)
        self.label_instruction.setStyleSheet("font-weight: bold; font-size: 18px; color: #333;")  # Bold text
        self.top_section.addWidget(self.label_instruction)
        
        self.btn_choose = QPushButton('Choose Image', self)
        self.btn_choose.clicked.connect(self.choose_image)
        # Style the button (rounded corners, primary color)
        self.btn_choose.setStyleSheet("border-radius: 10px; background-color: #4CAF50; color: white; padding: 10px 20px; font-size: 16px;")
        self.top_section.addWidget(self.btn_choose)

        # Image display section with centered label
        self.image_display = QHBoxLayout()
        self.image_display.setAlignment(Qt.AlignCenter)  # Center the image label
        self.layout.addLayout(self.image_display)

        self.label_image = QLabel(self)
        self.label_image.setFixedSize(250, 250)  # Fixed size for image display
        self.image_display.addWidget(self.label_image)

        # Options section with labels and radio buttons
        self.options_section = QVBoxLayout()
        self.layout.addLayout(self.options_section)

        self.label_options = QLabel('2. Choose an option', self)
        self.label_options.setStyleSheet("font-weight: bold; font-size: 18px; color: #333;")  # Bold text
        self.options_section.addWidget(self.label_options)

        self.option1 = QRadioButton('Apply Median Quantization', self)
        self.option1.setStyleSheet("font-size: 16px; color: #555;")
        self.option2 = QRadioButton('Apply Quantization + Bit Reduction', self)
        self.option2.setStyleSheet("font-size: 16px; color: #555;")
        self.options_section.addWidget(self.option1)
        self.options_section.addWidget(self.option2)

        # Process and save button
        self.btn_process = QPushButton('Process and Save Image', self)
        self.btn_process.clicked.connect(self.process_and_save_image)
        # Style the button (rounded corners, primary color)
        self.btn_process.setStyleSheet("border-radius: 10px; background-color: #4CAF50; color: white; padding: 10px 20px; font-size: 16px;")
        self.layout.addWidget(self.btn_process)

        self.image_path = None

    def choose_image(self):
        options = QFileDialog.Options()
        self.image_path, _ = QFileDialog.getOpenFileName(self, 'Select Image', '', 'Image Files (*.png *.jpg *.jpeg);;All Files (*)', options=options)
        if self.image_path:
            pixmap = QPixmap(self.image_path)
            self.label_image.setPixmap(pixmap.scaled(250, 250, Qt.KeepAspectRatio))

    def process_and_save_image(self):
        if not self.image_path:
            QMessageBox.warning(self, 'Error', 'Please select an image first.')
            return
        
        option = 1 if self.option1.isChecked() else 2 if self.option2.isChecked() else None
        if option is None:
            QMessageBox.warning(self, 'Error', 'Please choose an option.')
            return
        
        img = Image.open(self.image_path)
        img_array = np.array(img.convert('L'))  # Convert to grayscale
        
        if option == 1:
            processed_img_array = apply_median_quantization(img_array)
        elif option == 2:
            quantized_array = apply_median_quantization(img_array)
            processed_img_array = apply_bit_reduction(quantized_array)
        
        processed_img = Image.fromarray(processed_img_array)
        
        save_as, _ = QFileDialog.getSaveFileName(self, 'Save Image', '', 'PNG files (*.png);;JPEG files (*.jpeg);;All Files (*)')
        if save_as:
            processed_img.save(save_as)
            QMessageBox.information(self, 'Success', f'Image saved as {save_as}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageProcessor()
    ex.show()
    sys.exit(app.exec_())
