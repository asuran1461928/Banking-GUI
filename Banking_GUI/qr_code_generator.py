import tkinter as tk
from tkinter import ttk
import qrcode
from PIL import ImageTk, Image
import random

class QRCodeGenerator:
    def __init__(self, master, data, hide_random_id=True):
        self.master = master
        self.master.title("QR Code Generator")

        # Create a notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Style configuration for frames
        style = ttk.Style()
        style.configure('Red.TFrame', background='red')  # Set the background color to red

        # Frame for QR Code generation
        qr_frame = ttk.Frame(self.notebook, style='Red.TFrame')  # Use the custom style
        self.notebook.add(qr_frame, text="Generate QR Code")

        # Frame for navigation
        self.nav_frame = ttk.Frame(self.notebook, style='Blue.TFrame')  # Use a custom style for a blue background
        self.notebook.add(self.nav_frame, text="Navigation")

        # Generate a QR code
        random_id = generate_random_id()
        self.generate_qr_code(qr_frame, data, random_id)

        # Navigation buttons
        copy_button = tk.Button(self.nav_frame, text="Copy", command=lambda: self.copy_text(data))
        copy_button.configure(bg='blue', fg='white')  # Set background and foreground color
        copy_button.pack(pady=10)

        nav_button = tk.Button(self.nav_frame, text="Switch to QR Code Tab", command=lambda: self.notebook.select(0))
        nav_button.configure(bg='blue', fg='white')  # Set background and foreground color
        nav_button.pack(pady=10)

        # Show/hide random ID based on the 'hide_random_id' option
        self.random_id_visible = tk.BooleanVar()
        self.random_id_visible.set(not hide_random_id)  # Set the initial state

        self.label_random_id = tk.Label(self.nav_frame, text=f"Random ID: {random_id}")
        self.label_random_id.configure(bg='blue', fg='white')  # Set background and foreground color
        self.label_random_id.pack(pady=10)

        checkbutton_random_id = tk.Checkbutton(self.nav_frame, text="Show Random ID", variable=self.random_id_visible,
                                               command=self.toggle_random_id)
        checkbutton_random_id.configure(bg='blue', fg='white')  # Set background and foreground color
        checkbutton_random_id.pack(pady=10)

        # Initialize the random ID visibility based on the initial state
        self.toggle_random_id()

    def generate_qr_code(self, frame, data, random_id):
        # Generate a QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        # Create a QR code image
        img = qr.make_image(fill_color="black", back_color="white")
        img = img.resize((200, 200), resample=Image.BICUBIC)  # Use BICUBIC resampling
        img_tk = ImageTk.PhotoImage(img)  # Make img_tk an instance variable

        # Display the QR code image
        label_qr_code = tk.Label(frame, image=img_tk)
        label_qr_code.image = img_tk  # Keep a reference to avoid garbage collection
        label_qr_code.pack(padx=20, pady=10)

    def copy_text(self, text_to_copy):
        self.master.clipboard_clear()
        self.master.clipboard_append(text_to_copy)
        self.master.update()

    def toggle_random_id(self):
        if self.random_id_visible.get():
            # Show the random ID label
            self.label_random_id.pack(pady=10)
        else:
            # Remove the random ID label
            self.label_random_id.pack_forget()

def generate_random_id():
    # Generate a random ID (for demonstration purposes)
    return random.randint(1000, 9999)

if __name__ == "__main__":
    root = tk.Tk()
    generate_qr_code = QRCodeGenerator(root, "Test Data", hide_random_id=False)
    root.mainloop()
