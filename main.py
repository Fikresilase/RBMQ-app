import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QRadioButton, QVBoxLayout, QWidget, QMessageBox
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

def revert_bit_reduction(reduced_bit_image):
    """Revert from bit reduction (5 bits) to original quantized image."""
    reverted_image = np.left_shift(reduced_bit_image, 3)+4  # Reverting bit depth
    return reverted_image

class ImageProcessor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Image Processing App')
        self.setGeometry(100, 100, 800, 600)  # Larger window size
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout(self.central_widget)
        
        # Dark theme styling
        self.setStyleSheet(""" 
            QMainWindow { 
                background-color: #1e1e1e; 
            } 
            QLabel { 
                font-size: 18px; 
                font-weight: bold; 
                color: #ffffff; 
            } 
            QPushButton { 
                background-color: #4CAF50; 
                color: white; 
                border-radius: 10px; 
                padding: 12px; 
                font-size: 16px; 
                border: none; 
            } 
            QPushButton:hover { 
                background-color: #45a049; 
            } 
            QRadioButton { 
                font-size: 16px; 
                color: #ffffff; 
            } 
            #imageLabel { 
                background-color: #333; 
                border: 2px dashed #666; 
                min-width: 250px; 
                min-height: 250px; 
                display: flex; 
                justify-content: center; 
                align-items: center; 
            } 
            QMessageBox { 
                color: white; 
            } 
        """)
        
        # Add some spacing and centering for large screens
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(50, 50, 50, 50)
        
        self.label_instruction = QLabel('1. Select an image', self)
        self.label_instruction.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label_instruction)
        
        self.btn_choose = QPushButton('Choose Image', self)
        self.btn_choose.clicked.connect(self.choose_image)
        self.layout.addWidget(self.btn_choose, alignment=Qt.AlignCenter)
        
        self.label_image = QLabel(self)
        self.label_image.setObjectName("imageLabel")
        self.label_image.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label_image, alignment=Qt.AlignCenter)
        
        self.label_options = QLabel('2. Choose an option', self)
        self.label_options.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label_options)
        
        self.option1 = QRadioButton('Apply Median Quantization', self)
        self.option2 = QRadioButton('Apply Quantization + Bit Reduction', self)
        self.option3 = QRadioButton('Revert to Quantized Image', self)  # New option
        self.layout.addWidget(self.option1, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.option2, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.option3, alignment=Qt.AlignCenter)
        
        self.btn_process = QPushButton('Process and Save Image', self)
        self.btn_process.clicked.connect(self.process_and_save_image)
        self.layout.addWidget(self.btn_process, alignment=Qt.AlignCenter)
        
        self.image_path = None

    def choose_image(self):
        options = QFileDialog.Options()
        self.image_path, _ = QFileDialog.getOpenFileName(self, 'Select Image', '', 'Image Files (*.png *.jpg *.jpeg);;All Files (*)', options=options)
        if self.image_path:
            pixmap = QPixmap(self.image_path)
            self.label_image.setPixmap(pixmap.scaled(400, 400, Qt.KeepAspectRatio))  # Larger size for bigger screens

    def process_and_save_image(self):
        if not self.image_path:
            QMessageBox.warning(self, 'Error', 'Please select an image first.')
            return
        
        option = 1 if self.option1.isChecked() else 2 if self.option2.isChecked() else 3 if self.option3.isChecked() else None
        if option is None:
            QMessageBox.warning(self, 'Error', 'Please choose an option.')
            return
        
        try:
            img = Image.open(self.image_path)
            img_array = np.array(img)  # Get RGB values
            
            if img_array.ndim == 2:  # If grayscale, convert to RGB
                img_array = np.stack([img_array] * 3, axis=-1)
            
            r, g, b = img_array[:, :, 0], img_array[:, :, 1], img_array[:, :, 2]
            
            if option == 1:
                r_quant = apply_median_quantization(r)
                g_quant = apply_median_quantization(g)
                b_quant = apply_median_quantization(b)
                processed_img_array = np.stack([r_quant, g_quant, b_quant], axis=-1)
            elif option == 2:
                r_quant = apply_median_quantization(r)
                g_quant = apply_median_quantization(g)
                b_quant = apply_median_quantization(b)
                r_reduced = apply_bit_reduction(r_quant)
                g_reduced = apply_bit_reduction(g_quant)
                b_reduced = apply_bit_reduction(b_quant)
                processed_img_array = np.stack([r_reduced, g_reduced, b_reduced], axis=-1)
            elif option == 3:
                # r_quant = apply_median_quantization(r)
                # g_quant = apply_median_quantization(g)
                # b_quant = apply_median_quantization(b)
                # r_reduced = apply_bit_reduction(r_quant)
                # g_reduced = apply_bit_reduction(g_quant)
                # b_reduced = apply_bit_reduction(b_quant)
                r_reverted = revert_bit_reduction(r_reduced)
                g_reverted = revert_bit_reduction(g_reduced)
                b_reverted = revert_bit_reduction(b_reduced)
                processed_img_array = np.stack([r_reverted, g_reverted, b_reverted], axis=-1)
            
            processed_img = Image.fromarray(processed_img_array.astype(np.uint8))
            
            save_as, _ = QFileDialog.getSaveFileName(self, 'Save Image', '', 'PNG files (*.png);;JPEG files (*.jpeg);;All Files (*)')
            if save_as:
                processed_img.save(save_as)
                QMessageBox.information(self, 'Success', f'Image saved as {save_as}')
        
        except Exception as e:
            QMessageBox.critical(self, 'Error', f"An error occurred: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageProcessor()
    ex.show()
    sys.exit(app.exec_())
