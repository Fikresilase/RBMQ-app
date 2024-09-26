import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QRadioButton, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
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
    reverted_image = np.left_shift(reduced_bit_image, 3)+4 # Reverting bit depth
    return reverted_image
number = int(input("Enter a number: "))

# Apply the functions to the number
quantized_number = apply_median_quantization(number)
reduced_bit_number = apply_bit_reduction(quantized_number)
reverted_number = revert_bit_reduction(reduced_bit_number)

print("Quantized number:", quantized_number)
print("Reduced bit number:", reduced_bit_number)
print("Reverted number:", reverted_number)