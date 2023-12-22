import tkinter as tk
from qr_code_generator import QRCodeGenerator
from tkinter import Toplevel, Label, Entry, Button
from offline_transactions import OfflineTransactionsWindow
from offline_transactions import OfflineTransactionsWindow
from transaction_details import TransactionDetailsWindow

class BankingTab:
    def __init__(self, root, username):
        self.root = root
        self.username = username

        self.banking_window = tk.Toplevel(self.root)
        self.banking_window.title("Banking Details")

        button_size = 20
        window_width = button_size * 4 + 600
        window_height = button_size * 3 + 600
        self.banking_window.geometry(f"{window_width}x{window_height}")

        def create_colored_button(parent, color, text, row, column):
            def on_button_click():
                if text == "QR Code":
                    self.open_qr_code_window()
                elif text == "Offline Transactions":
                    self.open_offline_transactions_window()
                elif text == "Bank Statements":
                    self.open_transaction_details_window()
                else:
                    new_window = tk.Toplevel(self.banking_window)
                    new_window.title(f"Clicked: {text}")
                    label = tk.Label(new_window, text=f"You clicked {text}")
                    label.pack()

            button = tk.Button(parent, text=text, font=("Helvetica", 8), width=button_size, height=button_size,
                               bg=color, command=on_button_click)
            button.grid(row=row, column=column, sticky="nsew")
            parent.grid_rowconfigure(row, weight=1)
            parent.grid_columnconfigure(column, weight=1)

        create_colored_button(self.banking_window, "lightblue", "QR Code", 0, 0)
        create_colored_button(self.banking_window, "lightgreen", "Offline Transactions", 0, 1)
        create_colored_button(self.banking_window, "lightcoral", "Transaction History", 0, 2)
        create_colored_button(self.banking_window, "lightyellow", "Pay Bills", 1, 0)
        create_colored_button(self.banking_window, "lightpink", "Deposit", 1, 1)
        create_colored_button(self.banking_window, "lightgray", "Withdraw", 1, 2)
        create_colored_button(self.banking_window, "#FFA500", "Transfer", 2, 0)
        create_colored_button(self.banking_window, "lightgoldenrodyellow", "Check Balance", 2, 1)
        create_colored_button(self.banking_window, "lightcoral", "Bank Statements", 2, 2)

    def open_qr_code_window(self):
        data = f"Banking Details for {self.username}"
        qr_code_window = tk.Toplevel(self.banking_window)
        app = QRCodeGenerator(qr_code_window, data)

    def open_offline_transactions_window(self):
        offline_window = OfflineTransactionsWindow(self.banking_window, self.username)

    def open_transaction_details_window(self):
        # Example transaction details (replace with actual data)
        transactions = [
            {"timestamp": "2023-01-01 10:30:00", "details": "Transaction 1 details."},
            {"timestamp": "2023-01-02 15:45:00", "details": "Transaction 2 details."},
            # Add more transactions as needed
        ]
        TransactionDetailsWindow(self.banking_window, self.username, transactions)
if __name__ == "__main__":
    root = tk.Tk()
    app = BankingTab(root, "ExampleUser")
    root.mainloop()
