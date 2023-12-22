import tkinter as tk
from tkinter import ttk
import turtle
import random
import socket
from fpdf import FPDF
import uuid
import json
from banking_tab import BankingTab
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes

class BankingSystemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Banking System")
        self.root.geometry("800x600")  # Set your desired dimensions

        # Create a frame for navigation buttons at the top
        self.nav_frame = ttk.Frame(root)
        self.nav_frame.pack(side=tk.TOP, fill=tk.X)

        self.button_login = ttk.Button(self.nav_frame, text="Login", command=self.open_login_page)
        self.button_login.pack(side=tk.LEFT, padx=20)

        self.button_register = ttk.Button(self.nav_frame, text="Register", command=self.open_register_page)
        self.button_register.pack(side=tk.LEFT, padx=20)

        self.button_exit = ttk.Button(self.nav_frame, text="Exit", command=root.destroy)
        self.button_exit.pack(side=tk.RIGHT, padx=20)

        # Create and place widgets
        self.label_welcome = tk.Label(root, text="Welcome to Our Banking System", font=("Helvetica", 16))
        self.label_welcome.pack(pady=20)

        # Initialize Turtle for 3D animation and additional animations
        self.animation_canvas = turtle.ScrolledCanvas(root)
        self.animation_canvas.pack(fill=tk.BOTH, expand=True)
        self.turtle_3d = turtle.RawTurtle(self.animation_canvas)
        self.turtle_3d.speed(2)

        # Set the background color to black in the Turtle window
        self.animation_canvas.config(bg="black")

        # Create a list for geometric turtles
        self.geometric_turtles = []

        # Additional animation methods
        self.animate_flowers()

    def open_login_page(self):
        login_window = tk.Toplevel(self.root)
        login_window.title("Login")
        login_window.geometry("400x350")

        # Username and Password Entry Widgets
        label_username = tk.Label(login_window, text="Username:")
        label_username.pack(pady=10)
        entry_username = tk.Entry(login_window)
        entry_username.pack(pady=10)

        label_password = tk.Label(login_window, text="Password:")
        label_password.pack(pady=10)
        entry_password = tk.Entry(login_window, show="*")  # Show asterisks for password
        entry_password.pack(pady=10)

        # Checkbox for Scanning Physical Address
        scan_physical_address = tk.BooleanVar()
        check_physical_address = tk.Checkbutton(login_window, text="Scan Physical Address",
                                                variable=scan_physical_address)
        check_physical_address.pack(pady=10)

        # Submit Button
        submit_button = tk.Button(login_window, text="Submit",
                                  command=lambda: self.validate_login(entry_username.get(), entry_password.get(),
                                                                      scan_physical_address.get()))
        submit_button.pack(pady=20)

    def validate_login(self, username, password, scan_physical_address):
        # Check if the user exists and the provided credentials are correct
        if self.check_credentials(username, password):
            if scan_physical_address:
                entered_physical_address = self.get_physical_address()
                stored_physical_address = self.get_stored_physical_address(username)
                if entered_physical_address == stored_physical_address:
                    print("Login successful.")
                    self.open_banking_tab(username)
                else:
                    print("Physical address mismatch. Login failed.")
            else:
                print("Login successful.")
                self.open_banking_tab(username)
        else:
            print("Invalid credentials. Login failed.")

    def open_banking_tab(self, username):
        banking_tab = BankingTab(self.root, username)
        for window in self.root.winfo_children():
            if window != banking_tab.banking_window:
                window.destroy()

    def check_credentials(self, username, password):
        # Include your logic to check the credentials against the stored data
        # This could involve reading from a file or querying a database
        # For simplicity, let's assume a simple dictionary as a data store
        with open("registration_data.json", "r") as file:
            for line in file:
                user_data = json.loads(line)
                if user_data["Username"] == username and user_data["Password"] == password:
                    return True
        return False

    def get_stored_physical_address(self, username):
        # Include your logic to retrieve the stored physical address for a given username
        # This could involve reading from a file or querying a database
        # For simplicity, let's assume a simple dictionary as a data store
        with open("registration_data.json", "r") as file:
            for line in file:
                user_data = json.loads(line)
                if user_data["Username"] == username:
                    return user_data.get("Physical Address", None)
        return None



    def get_stored_physical_address(self, username):
        # Include your logic to retrieve the stored physical address for a given username
        # This could involve reading from a file or querying a database
        # For simplicity, let's assume a simple dictionary as a data store
        with open("registration_data.json", "r") as file:
            for line in file:
                user_data = json.loads(line)
                if user_data["Username"] == username:
                    return user_data.get("Physical Address", None)
        return None

    def open_register_page(self):
        register_window = tk.Toplevel(self.root)
        register_window.title("Register")
        register_window.geometry("400x550")

        registration_frame = ttk.LabelFrame(register_window, text="Registration Details")
        registration_frame.pack(pady=20, padx=10, fill=tk.BOTH, expand=True)

        label_username = tk.Label(registration_frame, text="Username:")
        label_username.grid(row=0, column=0, pady=10)
        entry_username = tk.Entry(registration_frame)
        entry_username.grid(row=0, column=1, pady=10)

        label_password = tk.Label(registration_frame, text="Password:")
        label_password.grid(row=1, column=0, pady=10)
        entry_password = tk.Entry(registration_frame, show="*")
        entry_password.grid(row=1, column=1, pady=10)

        label_confirm_password = tk.Label(registration_frame, text="Confirm Password:")
        label_confirm_password.grid(row=2, column=0, pady=10)
        entry_confirm_password = tk.Entry(registration_frame, show="*")
        entry_confirm_password.grid(row=2, column=1, pady=10)

        label_email = tk.Label(registration_frame, text="Email:")
        label_email.grid(row=3, column=0, pady=10)
        entry_email = tk.Entry(registration_frame)
        entry_email.grid(row=3, column=1, pady=10)

        label_phone = tk.Label(registration_frame, text="Phone Number:")
        label_phone.grid(row=4, column=0, pady=10)

        country_code_combobox = ttk.Combobox(registration_frame, values=["+1", "+44", "+91", "+81", "+86"], width=5)
        country_code_combobox.set("+1")
        country_code_combobox.grid(row=4, column=1, padx=5)

        entry_phone_number = tk.Entry(registration_frame)
        entry_phone_number.grid(row=4, column=2, pady=10)

        label_bank_account = tk.Label(registration_frame, text="Bank Account Number:")
        label_bank_account.grid(row=6, column=0, pady=10)
        entry_bank_account = tk.Entry(registration_frame)
        entry_bank_account.grid(row=6, column=1, pady=10)

        scan_physical_address_var = tk.BooleanVar()
        check_physical_address = tk.Checkbutton(registration_frame, text="Scan Physical Address",
                                                variable=scan_physical_address_var)
        check_physical_address.grid(row=7, columnspan=2, pady=10)

        scan_physical_address_var = tk.BooleanVar()
        check_physical_address = tk.Checkbutton(registration_frame, text="Scan Physical Address",
                                                variable=scan_physical_address_var)
        check_physical_address.grid(row=5, columnspan=2, pady=10)

        def process_registration():
            username = entry_username.get()
            password = entry_password.get()
            confirm_password = entry_confirm_password.get()
            email = entry_email.get()
            phone_number = f"{country_code_combobox.get()} {entry_phone_number.get()}"
            scan_physical_address = scan_physical_address_var.get()

            if scan_physical_address:
                physical_address = self.get_physical_address()
            else:
                physical_address = None

            # Generate a wallet and key pair
            wallet, private_key = self.generate_wallet()

            # Save registration information with wallet and public key
            self.save_registration_info(username, password, confirm_password, email, phone_number,
                                        physical_address, wallet, private_key)

        submit_button = tk.Button(register_window, text="Register", command=process_registration)
        submit_button.pack(pady=20)
        submit_button.config(bg="blue", fg="white")

    def get_physical_address(self):
        try:
            physical_address = socket.gethostbyname(socket.gethostname())
            return physical_address
        except Exception as e:
            print("Error getting physical address:", e)
            return None

    def generate_wallet(self):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

        public_key = private_key.public_key()

        # Serialize public key for storage
        public_key_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        # Generate a unique identifier for the wallet
        wallet_id = str(uuid.uuid4())

        wallet = {
            'id': wallet_id,
            'public_key': public_key_bytes.decode('utf-8'),
            'balance': 0
        }

        return wallet, private_key
    def save_registration_info(self, username, password, confirm_password, email, phone_number, physical_address,wallet, private_key,bank_account_number):
        registration_data = {
            "Username": username,
            "Password": password,
            "Confirm Password": confirm_password,
            "Email": email,
            "Phone Number": phone_number,
            "Physical Address": physical_address,
            "Wallet": wallet,
            "Bank Account Number": bank_account_number
        }

        with open("registration_data.json", "a") as file:
            json.dump(registration_data, file)
            file.write("\n")

        print("Registration information saved.")

    def animate_flowers(self):
        # Schedule the continuous creation of flowers
        self.create_flower()
        self.root.after(500, self.animate_flowers)  # Adjust the time interval (in milliseconds)

    def create_flower(self):
        x_position = random.randint(-200, 200)
        y_position = random.randint(-200, 200)

        self.draw_flower(x_position, y_position)

        self.animation_canvas.update()

    def draw_flower(self, x, y):
        flower_turtle = turtle.RawTurtle(self.animation_canvas)
        flower_turtle.speed(0)
        flower_turtle.penup()
        flower_turtle.goto(x, y)
        flower_turtle.pendown()

        # Draw petals
        for _ in range(6):
            flower_turtle.color(random.random(), random.random(), random.random())
            flower_turtle.begin_fill()
            flower_turtle.circle(20, 60)
            flower_turtle.left(120)
            flower_turtle.circle(20, 60)
            flower_turtle.end_fill()
            flower_turtle.left(60)

        # Draw the center
        flower_turtle.color("yellow")
        flower_turtle.begin_fill()
        flower_turtle.circle(5)
        flower_turtle.end_fill()

        self.geometric_turtles.append(flower_turtle)

    def destroy_additional_turtles(self):
        # Destroy additional turtles to clear the canvas
        for turtle_obj in self.geometric_turtles:
            turtle_obj.clear()
            turtle_obj.hideturtle()

if __name__ == "__main__":
    root = tk.Tk()
    app = BankingSystemGUI(root)
    root.mainloop()
