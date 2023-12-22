# pdf_generator/pdf_generator.py

from fpdf import FPDF
from datetime import datetime
import os

class PDFGenerator:
    def __init__(self, username, transaction_details):
        self.username = username
        self.transaction_details = transaction_details

        self.generate_pdf()

    def generate_pdf(self):
        pdf = FPDF()
        pdf.add_page()

        # Set font
        pdf.set_font("Arial", size=12)

        # Add content to the PDF (adjust as needed)
        pdf.cell(200, 10, txt=f"Bank Statement for {self.username}", ln=True, align='C')
        pdf.cell(200, 10, txt="", ln=True)  # Add an empty line

        # Add bank policies
        bank_policies = """
        Welcome to Our Bank!

        Our Policies:
        1. Your security is our top priority.
        2. Keep your account information confidential.
        3. Contact customer support for any assistance.
        """
        pdf.multi_cell(0, 10, txt=bank_policies)

        pdf.cell(200, 10, txt="", ln=True)  # Add an empty line

        # Add sender and receiver information
        sender_info = "Sender: John Doe\nBank Number: XXXX-XXXX-XXXX-XXXX\nIFSC Code: ABCD123456"
        receiver_info = "Receiver: Jane Doe\nBank Number: YYYY-YYYY-YYYY-YYYY\nIFSC Code: EFGH789012"
        pdf.multi_cell(0, 10, txt=f"{sender_info}\n{receiver_info}")

        pdf.cell(200, 10, txt="", ln=True)  # Add an empty line

        # Add text watermark
        pdf.set_text_color(200, 200, 200)
        pdf.set_font("Arial", style="I", size=60)
        pdf.text(10, 140, "Watermark")

        pdf.cell(200, 10, txt="", ln=True)  # Add an empty line

        # Add transaction details
        pdf.cell(200, 10, txt="Transaction Details:", ln=True)

        for transaction in self.transaction_details:
            pdf.cell(200, 10, txt=f"{transaction['timestamp']} - {transaction['details']}", ln=True)

        # Save the PDF to a file
        file_name = f"bank_statement_{self.username}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
        pdf.output(file_name)

        # Provide a link for download (modify as needed based on your platform)
        download_link = f"<a href='{file_name}' download>Download PDF</a>"
        print(f"PDF generated: {file_name}")
        print(f"Download link: {download_link}")

        os.startfile(file_name)

if __name__ == "__main__":
    # Example usage
    # Replace 'username' with the actual username
    pdf_generator = PDFGenerator("ExampleUser")
