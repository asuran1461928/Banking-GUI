# transaction_details.py

import tkinter as tk
from pdf_generator import PDFGenerator  # Correct import statement

class TransactionDetailsWindow:
    def __init__(self, parent, username, transaction_details):
        self.parent = parent
        self.username = username
        self.transaction_details = transaction_details

        self.open_window()

    def open_window(self):
        transaction_window = tk.Toplevel(self.parent)
        transaction_window.title("Transaction Details")

        # Set a larger window size
        window_width = 600
        window_height = 400
        transaction_window.geometry(f"{window_width}x{window_height}")

        # Create UI elements and display transaction details
        for transaction in self.transaction_details:
            label = tk.Label(transaction_window, text=f"{transaction['timestamp']} - {transaction['details']}")
            label.pack()

            # Add a button to generate PDF for each transaction
            pdf_button = tk.Button(transaction_window, text=f"Generate PDF for {transaction['timestamp']}",
                                   command=lambda t=transaction: self.generate_pdf(t))
            pdf_button.pack()

    def generate_pdf(self, transaction):
        # Pass the username and selected transaction details to the PDF generator
        pdf_generator = PDFGenerator(self.username, [transaction])

        download_button = tk.Button(self.parent, text="Download PDF", command=lambda: self.download_pdf(pdf_generator))
        download_button.pack()

    def download_pdf(self, pdf_generator):
        # Implement the logic to handle the download (e.g., save the file to a specific location)
        pdf_generator.generate_pdf()
        # You might want to give feedback to the user that the download is complete.
        print("PDF downloaded.")

if __name__ == "__main__":
    # Example usage
    # Replace 'username' and 'transactions' with actual values
    window = tk.Tk()
    transactions = [
        {"timestamp": "2023-01-01 10:30:00", "details": "Transaction 1 details."},
        {"timestamp": "2023-01-02 15:45:00", "details": "Transaction 2 details."},
        # Add more transactions as needed
    ]
    app = TransactionDetailsWindow(window, "ExampleUser", transactions)
    window.mainloop()
