import tkinter as tk
from tkinter import Toplevel, Label, Entry, Button, messagebox, Text, Scrollbar, END
import sqlite3
from datetime import datetime
import threading
import time


class NavigationBar:
    def __init__(self, parent, go_back_func):
        self.parent = parent

        self.nav_frame = tk.Frame(self.parent)
        self.nav_frame.pack(side=tk.TOP, fill=tk.X)

        self.go_back_button = tk.Button(self.nav_frame, text="Go Back", command=go_back_func, bg="blue", fg="white")
        self.go_back_button.pack(side=tk.LEFT, padx=20)


class ChatWindow:
    def __init__(self, parent, username, db_connection, transaction_callback):
        self.parent = parent
        self.username = username
        self.db_connection = db_connection
        self.transaction_callback = transaction_callback

        self.chat_window = Toplevel(self.parent)
        self.chat_window.title(f"Chat with {self.username}")

        self.chat_text = Text(self.chat_window, height=10, width=50)
        self.chat_text.pack(pady=10)

        self.scrollbar = Scrollbar(self.chat_window)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.chat_text.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.chat_text.yview)

        self.message_entry = Entry(self.chat_window, width=50)
        self.message_entry.pack(pady=10)

        send_button = Button(self.chat_window, text="Send", command=self.send_message, bg="blue", fg="white")
        send_button.pack(pady=10)

    def send_message(self):
        amount = self.message_entry.get()  # For simplicity, using the message entry for the transaction amount
        if amount:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.chat_text.insert(END, f"{timestamp} You: Sent {amount} to {self.username}\n")

            # Save the transaction to the local database
            self.save_transaction_to_db("You", self.username, float(amount), timestamp)

            # Notify the recipient (simulate real-time)
            threading.Thread(target=self.transaction_callback, args=(self.username, float(amount), timestamp)).start()

    def save_transaction_to_db(self, sender, recipient, amount, timestamp):
        cursor = self.db_connection.cursor()
        cursor.execute("INSERT INTO transactions (sender, recipient, amount, timestamp) VALUES (?, ?, ?, ?)",
                       (sender, recipient, amount, timestamp))
        self.db_connection.commit()


class PaymentRequestWindow:
    def __init__(self, parent, username, db_connection, transaction_callback):
        self.parent = parent
        self.username = username
        self.db_connection = db_connection
        self.transaction_callback = transaction_callback

        self.payment_request_window = Toplevel(self.parent)
        self.payment_request_window.title("Payment Request")

        label_instruction = Label(self.payment_request_window, text=f"Payment Request for {self.username}")
        label_instruction.pack(pady=10)

        # Amount Entry
        label_amount = Label(self.payment_request_window, text="Amount:")
        label_amount.pack(pady=5)
        self.entry_amount = Entry(self.payment_request_window)
        self.entry_amount.pack(pady=5)

        # Pay and Receive Buttons
        pay_button = Button(self.payment_request_window, text="Pay", command=self.pay, bg="blue", fg="white")
        pay_button.pack(side=tk.LEFT, padx=10)

        receive_button = Button(self.payment_request_window, text="Receive", command=self.receive, bg="blue",
                                fg="white")
        receive_button.pack(side=tk.RIGHT, padx=10)

        # Chat Button
        chat_button = Button(self.payment_request_window, text="Chat", command=self.open_chat, bg="blue", fg="white")
        chat_button.pack(pady=10)

        # Chat Window
        self.chat_window = ChatWindow(self.parent, self.username, self.db_connection, self.transaction_callback)
        self.chat_window.chat_window.withdraw()

    def pay(self):
        amount = self.entry_amount.get()
        messagebox.showinfo("Payment", f"Paid {amount} to {self.username}")

    def receive(self):
        amount = self.entry_amount.get()
        messagebox.showinfo("Payment", f"Requested {amount} from {self.username}")

    def open_chat(self):
        self.chat_window.chat_window.deiconify()


class OfflineTransactionsWindow:
    def __init__(self, parent, username):
        self.parent = parent
        self.username = username

        # Initialize the local database
        self.db_connection = sqlite3.connect("offline_transactions.db")
        self.create_tables()

        self.offline_window = Toplevel(self.parent)
        self.offline_window.title("Offline Transactions")
        self.offline_window.configure(bg="red")  # Set default background color

        # Set the window size
        window_width = 400
        window_height = 450
        self.offline_window.geometry(f"{window_width}x{window_height}")

        self.navigation_bar = NavigationBar(self.offline_window, self.go_back)

        label_instruction = Label(self.offline_window, text="Enter Offline Transactions Details:", bg="red")
        label_instruction.pack(pady=10)

        # Predefined Bank Account Number for Verification
        self.predefined_bank_account = "123456789"

        # Bank Account Number
        label_bank_account = Label(self.offline_window, text="Bank Account Number:", bg="red")
        label_bank_account.pack(pady=5)
        self.entry_bank_account = Entry(self.offline_window)
        self.entry_bank_account.pack(pady=5)

        # Rebank Account Number
        label_rebank_account = Label(self.offline_window, text="Re-enter Bank Account Number:", bg="red")
        label_rebank_account.pack(pady=5)
        self.entry_rebank_account = Entry(self.offline_window)
        self.entry_rebank_account.pack(pady=5)

        # IFSC Code
        label_ifsc_code = Label(self.offline_window, text="IFSC Code:", bg="red")
        label_ifsc_code.pack(pady=5)
        self.entry_ifsc_code = Entry(self.offline_window)
        self.entry_ifsc_code.pack(pady=5)

        # Account Holder's Name
        label_account_holder_name = Label(self.offline_window, text="Account Holder's Name:", bg="red")
        label_account_holder_name.pack(pady=5)
        self.entry_account_holder_name = Entry(self.offline_window)
        self.entry_account_holder_name.pack(pady=5)

        # Phone Number
        label_phone_number = Label(self.offline_window, text="Phone Number:", bg="red")
        label_phone_number.pack(pady=5)
        self.entry_phone_number = Entry(self.offline_window)
        self.entry_phone_number.pack(pady=5)

        # Verify Button
        self.verify_button = Button(self.offline_window, text="Verify", command=self.verify_details, bg="blue",
                                    fg="white")
        self.verify_button.pack(pady=20)

        # Payment Request Window (initialized but not displayed)
        self.payment_request_window = PaymentRequestWindow(
            self.offline_window, self.username, self.db_connection, self.notify_transaction)
        self.payment_request_window.payment_request_window.withdraw()

    def verify_details(self):
        # Get the provided values from input fields
        entered_bank_account = self.entry_bank_account.get()
        entered_rebank_account = self.entry_rebank_account.get()
        entered_ifsc_code = self.entry_ifsc_code.get()
        entered_account_holder_name = self.entry_account_holder_name.get()
        entered_phone_number = self.entry_phone_number.get()

        # Check if all input fields are filled
        if not all(
            [entered_bank_account, entered_rebank_account, entered_ifsc_code, entered_account_holder_name,
             entered_phone_number]):
            messagebox.showerror("Input Error", "Please fill in all required fields.")
            return

        # Check if the entered bank account number matches the predefined value
        if entered_bank_account == self.predefined_bank_account:
            messagebox.showinfo("Verification", "Details Verified Successfully!")
            # Change background color to green on successful verification
            self.offline_window.configure(bg="green")
            # Display Payment Request Window
            self.payment_request_window.payment_request_window.deiconify()
        else:
            messagebox.showerror("Verification Error", "Invalid Bank Account Number!")

    def go_back(self):
        # Hide Payment Request Window before going back
        self.payment_request_window.payment_request_window.withdraw()
        self.offline_window.destroy()

    def create_tables(self):
        cursor = self.db_connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS transactions
                          (sender TEXT, recipient TEXT, amount REAL, timestamp TEXT)''')
        self.db_connection.commit()

    def notify_transaction(self, recipient, amount, timestamp):
        self.payment_request_window.chat_window.chat_text.insert(
            END, f"{timestamp} {recipient}: Received {amount} from you\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = OfflineTransactionsWindow(root, "ExampleUser")
    root.mainloop()
