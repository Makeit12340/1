"""
------------------------------------------------------------
TCP Selective Group Chat Client
Computer Networks Laboratory
------------------------------------------------------------
"""

import socket
import threading

# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

HOST = "127.0.0.1"
PORT = 5000
BUFFER_SIZE = 1024

# ---------------------------------------------------------
# Create Socket
# ---------------------------------------------------------

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

print("=" * 60)
print("      TCP SELECTIVE GROUP CHAT CLIENT")
print("=" * 60)

username = input("Enter Username : ").strip()

# Send login request
client.send(f"LOGIN|{username}".encode())

online_users = []

# ---------------------------------------------------------
# Receive Messages
# ---------------------------------------------------------

def receive_messages():

    global online_users

    while True:

        try:

            packet = client.recv(BUFFER_SIZE).decode()

            if not packet:
                break

            parts = packet.split("|", 2)
            command = parts[0]

            # -----------------------------
            # Login / Info Messages
            # -----------------------------

            if command == "INFO":

                print(f"\\n[INFO] {parts[1]}")

            # -----------------------------
            # Error Messages
            # -----------------------------

            elif command == "ERROR":

                print(f"\\n[ERROR] {parts[1]}")

            # -----------------------------
            # Online Users
            # -----------------------------

            elif command == "USERS":

                if len(parts) > 1 and parts[1]:
                    online_users = parts[1].split(",")
                else:
                    online_users = []

                print("\\nOnline Users")
                print("---------------------")

                for user in online_users:
                    print(user)

            # -----------------------------
            # Incoming Chat Message
            # -----------------------------

            elif command == "MSG":

                sender = parts[1]
                message = parts[2]

                print("\\n----------------------------------")
                print(f"From : {sender}")
                print(f"Message : {message}")
                print("----------------------------------")

        except:

            print("\\nDisconnected from server.")
            break


# ---------------------------------------------------------
# Send Messages
# ---------------------------------------------------------

def send_messages():

    while True:

        print("\\nRecipients (comma separated)")
        receivers = input("> ")

        if receivers.lower() == "exit":

            client.send(f"EXIT|{username}".encode())
            break

        message = input("Message : ")

        packet = f"SEND|{username}|{receivers}|{message}"

        client.send(packet.encode())

    client.close()


# ---------------------------------------------------------
# Start Threads
# ---------------------------------------------------------

receive_thread = threading.Thread(target=receive_messages)
send_thread = threading.Thread(target=send_messages)

receive_thread.start()
send_thread.start()

receive_thread.join()
send_thread.join()

print("\\nConnection Closed.")
