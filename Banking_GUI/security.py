import random
import datetime
import numpy
import pygame
import math
from twilio.rest import Client
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from playsound import playsound  # Import playsound
import requests
from io import BytesIO
import matplotlib.pyplot as plt
from PIL import Image
import IPython.display as display

from IPython.display import display, Image
from IPython.display import Image

# Specify the path to your downloaded GIF file
gif_path = '/Users/macos/PycharmProjects/otis/venv/sonar-radar.gif'

# Display the GIF
Image(filename=gif_path)

# Path to the email sent sound file
email_sent_sound = 'email_sent.mp3'

# Twilio credentials
account_sid = 'ACa6202649c215880510aa4dd558abbf6b'
auth_token = '6dd5107af2bbcaa552a05489b20381de'
twilio_phone_number = '+12294145803'
recipient_phone_number = '+918978796351'

# Email credentials
email_address = 'roguem777@gmail.com'  # Replace with your email address
email_password = 'olne hsus xdck gzoo'  # Replace with your email password

# Initialize Twilio client
client = Client(account_sid, auth_token)

class FraudDetectionSystem:
    def __init__(self):
        self.known_users = {}  # Simulated user database
        self.alerts = []
        self.fraud_links = set()  # Simulated list of known fraudulent links

    def register_user(self, user_id):
        if user_id not in self.known_users:
            self.known_users[user_id] = {
                'balance': random.uniform(1000, 100000),
                'transactions': [],
                'last_login': datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 30))
            }

    def add_transaction(self, user_id, amount):
        if user_id in self.known_users:
            self.known_users[user_id]['transactions'].append(amount)

    def detect_fraud(self, user_id):
        if user_id in self.known_users:
            user = self.known_users[user_id]
            transactions = user['transactions']

            # Rule 1: Abnormally large transaction
            if transactions and transactions[-1] > 10000:
                self.alerts.append(
                    f"ALERT: Suspicious large transaction for user {user_id}. Amount: {transactions[-1]}")

            # Rule 2: Frequent logins
            if (datetime.datetime.now() - user['last_login']).days < 7:
                self.alerts.append(f"ALERT: Unusually frequent logins for user {user_id}")

    def detect_fraudulent_link_click(self, user_id, link):
        if user_id in self.known_users and link in self.fraud_links:
            self.alerts.append(f"ALERT: User {user_id} clicked on a known fraudulent link: {link}")
            # Play a sound when a fraudulent link is clicked
            playsound('/Users/macos/PycharmProjects/otis/venv/alert.mp3')

    def report_fraud(self):
        for alert in self.alerts:
            print(alert)

    def user_feedback(self, user_id, feedback):
        # In a real system, this feedback would be logged and reviewed by fraud analysts.
        print(f"User {user_id} reported: {feedback}")

    def make_phone_call(self, user_id, message):
        try:
            call = client.calls.create(
                to=recipient_phone_number,
                from_=twilio_phone_number,
                url='http://demo.twilio.com/docs/voice.xml',  # You can use your own TwiML for more customization.
                method='GET'
            )
            print(f"Call SID for user {user_id}: {call.sid}")
        except Exception as e:
            print("Error:", str(e))

    def send_email(self, user_id, subject, body):
        sender_email = email_address
        receiver_email = 'Karthikeyaa.official@gmail.com'  # Replace with the recipient's email address

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, email_password)
                server.sendmail(sender_email, receiver_email, message.as_string())
                print("Email sent successfully.")
                # Play a sound when email is sent
                playsound('/Users/macos/PycharmProjects/otis/venv/alert.mp3')
        except Exception as e:
            print("Error:", str(e))

    def monitor_information_flow(self, user_id, source, destination, data):
        # Log information flow
        log_entry = f"User {user_id} shared data from {source} to {destination}: {data}"
        print(log_entry)

        # Add any fraud detection logic here (e.g., suspicious patterns or blacklisted destinations)

if __name__ == "__main__":
    fraud_system = FraudDetectionSystem()

    for _ in range(20):
        user_id = random.randint(1000, 9999)
        transaction_amount = random.uniform(1, 20000)
        fraud_system.register_user(user_id)
        fraud_system.add_transaction(user_id, transaction_amount)
        fraud_system.detect_fraud(user_id)

    fraud_system.report_fraud()

    # Simulate user reporting a suspicious activity, send an email, and make a phone call
    user_id = random.choice(list(fraud_system.known_users.keys()))
    feedback = "I noticed a large transaction on my account."
    fraud_system.user_feedback(user_id, feedback)

    email_subject = "Suspicious Activity Report"
    email_body = "Hello,\nA user has reported suspicious activity on their account."
    fraud_system.send_email(user_id, email_subject, email_body)
    fraud_system.make_phone_call(user_id,
                                 "Hello, this is the Fraud Detection Bot. A suspicious transaction has been detected on your account. Please review your recent transactions and report any unauthorized activity.")

    # Simulate information flow monitoring
    source = "App A"
    destination = "User B"
    data = "Sensitive data"
    fraud_system.monitor_information_flow(user_id, source, destination, data)