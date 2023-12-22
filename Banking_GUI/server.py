# server.py
import socket
import threading
import sqlite3
from datetime import datetime

def handle_client(client_socket, db_connection):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"Received message: {message}")

            # Save the message to the local database
            save_message_to_db("Client", "Server", message, timestamp, db_connection)

            # Send the message back to the client
            client_socket.send(f"Server: {message}".encode('utf-8'))

        except Exception as e:
            print(f"Error handling client: {e}")
            break

    client_socket.close()


def save_message_to_db(recipient, sender, message, timestamp, db_connection):
    cursor = db_connection.cursor()
    cursor.execute("INSERT INTO messages (recipient, sender, message, timestamp) VALUES (?, ?, ?, ?)",
                   (recipient, sender, message, timestamp))
    db_connection.commit()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 12345))
    server.listen(5)

    print("Server listening on port 12345")

    db_connection = sqlite3.connect("offline_transactions_server.db")
    create_tables(db_connection)

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")

        client_handler = threading.Thread(target=handle_client, args=(client_socket, db_connection))
        client_handler.start()


def create_tables(db_connection):
    cursor = db_connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS messages
                      (recipient TEXT, sender TEXT, message TEXT, timestamp TEXT)''')
    db_connection.commit()


if __name__ == "__main__":
    start_server()
