import os
from tkinter import Tk, filedialog, Button, Label, Radiobutton, IntVar, messagebox
from PIL import Image, ImageTk
import numpy as np

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

def process_image(file_path, option):
    # Load the image and convert it to a NumPy array
    img = Image.open(file_path)
    img_array = np.array(img)

    # Apply the selected processing option
    if option == 1:
        processed_img_array = apply_median_quantization(img_array)
    elif option == 2:
        quantized_array = apply_median_quantization(img_array)
        processed_img_array = apply_bit_reduction(quantized_array)
    else:
        return None

    # Convert the processed array back to an image
    processed_img = Image.fromarray(processed_img_array)
    return processed_img

def save_image(processed_img, original_path):
    # Get the directory and filename
    directory, file_name = os.path.split(original_path)
    file_name_no_ext, ext = os.path.splitext(file_name)

    # Ask the user for the file format they want to save
    save_as = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpeg"), ("All files", "*.*")]
    )
    
    # Save the processed image in the selected format
    if save_as:
        processed_img.save(save_as)
        messagebox.showinfo("Success", f"Image saved as {save_as}")

def choose_image():
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png;*.jpeg;*.jpg"), ("All Files", "*.*")]
    )
    if file_path:
        img = Image.open(file_path)
        img.thumbnail((250, 250))  # Resize for display purposes
        img_tk = ImageTk.PhotoImage(img)
        label_image.config(image=img_tk)
        label_image.image = img_tk
        label_image.file_path = file_path

def process_and_save_image():
    if not hasattr(label_image, 'file_path'):
        messagebox.showerror("Error", "Please select an image first.")
        return

    option = var.get()
    if option == 0:
        messagebox.showerror("Error", "Please choose an option.")
        return

    processed_img = process_image(label_image.file_path, option)
    if processed_img:
        save_image(processed_img, label_image.file_path)

# GUI Setup
root = Tk()
root.title("Image Processing App")

var = IntVar()  # For radio button option

label_instruction = Label(root, text="1. Select an image")
label_instruction.pack()

btn_choose = Button(root, text="Choose Image", command=choose_image)
btn_choose.pack()

label_image = Label(root)
label_image.pack()

label_options = Label(root, text="2. Choose an option")
label_options.pack()

radio1 = Radiobutton(root, text="Apply Median Quantization", variable=var, value=1)
radio1.pack()

radio2 = Radiobutton(root, text="Apply Quantization + Bit Reduction", variable=var, value=2)
radio2.pack()

btn_process = Button(root, text="Process and Save Image", command=process_and_save_image)
btn_process.pack()

root.mainloop()
