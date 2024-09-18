import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PIL import Image

def revert_bit_reduction(color_channel):
    """Revert from bit reduction (5 bits) to original color channel."""
    reverted_channel = np.left_shift(color_channel, 3)  # Revert the bit depth reduction
    return reverted_channel

class ColorImageReverter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    

    def initUI(self):
        self.setWindowTitle('Color Image Reverter App')
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

        self.label_instruction = QLabel('1. Select a previously processed color image (bit-reduced)', self)
        self.label_instruction.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label_instruction)

        self.btn_choose = QPushButton('Choose Image', self)
        self.btn_choose.clicked.connect(self.choose_image)
        self.layout.addWidget(self.btn_choose, alignment=Qt.AlignCenter)

        self.label_image = QLabel(self)
        self.label_image.setObjectName("imageLabel")
        self.label_image.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label_image, alignment=Qt.AlignCenter)

        self.btn_revert = QPushButton('Revert and Save Image', self)
        self.btn_revert.clicked.connect(self.revert_and_save_image)
        self.layout.addWidget(self.btn_revert, alignment=Qt.AlignCenter)

        self.image_path = None

    def choose_image(self):
        options = QFileDialog.Options()
        self.image_path, _ = QFileDialog.getOpenFileName(self, 'Select Image', '', 'Image Files (*.png *.jpg *.jpeg);;All Files (*)', options=options)
        if self.image_path:
            pixmap = QPixmap(self.image_path)
            self.label_image.setPixmap(pixmap.scaled(400, 400, Qt.KeepAspectRatio))  # Larger size for bigger screens

    


    def revert_and_save_image(self):
        if not self.image_path:
            QMessageBox.warning(self, 'Error', 'Please select an image first.')
            return

        img = Image.open(self.image_path)
        img_array = np.array(img)  # Convert image to array
        
        if len(img_array.shape) == 3:  # Check if image has color channels (RGB)
            # Separate the channels
            r_channel = img_array[:, :, 0]
            g_channel = img_array[:, :, 1]
            b_channel = img_array[:, :, 2]

            # Revert the bit reduction for each channel
            reverted_r = revert_bit_reduction(r_channel)
            reverted_g = revert_bit_reduction(g_channel)
            reverted_b = revert_bit_reduction(b_channel)

            # Merge the channels back together
            reverted_img_array = np.stack((reverted_r, reverted_g, reverted_b), axis=2)
        else:
            QMessageBox.warning(self, 'Error', 'The selected image is not a color image.')
            return

        reverted_img = Image.fromarray(reverted_img_array.astype(np.uint8))  # Convert back to an image

        save_as, _ = QFileDialog.getSaveFileName(self, 'Save Image', '', 'PNG files (*.png);;JPEG files (*.jpeg);;All Files (*)')
        if save_as:
            reverted_img.save(save_as)
            QMessageBox.information(self, 'Success', f'Image saved as {save_as}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ColorImageReverter()
    ex.show()
    sys.exit(app.exec_())

    def choose_image(self):
        try:
            options = QFileDialog.Options()
            self.image_path, _ = QFileDialog.getOpenFileName(self, 'Select Image', '', 'Image Files (*.png *.jpg *.jpeg);;All Files (*)', options=options)
            if self.image_path:
                pixmap = QPixmap(self.image_path)
            self.label_image.setPixmap(pixmap.scaled(400, 400, Qt.KeepAspectRatio))  # Larger size for bigger screens
        except Exception as e:
            QMessageBox.critical(self, 'Error', f"Failed to load image: {e}")
