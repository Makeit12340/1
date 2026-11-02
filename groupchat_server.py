"""
------------------------------------------------------------
TCP Selective Group Chat Server
Computer Networks Laboratory

Features
--------
1. Multiple clients
2. Private Messaging
3. Group Messaging
4. Online User List
5. Graceful Client Disconnect
6. Server Exit (only if no clients are connected)

Author : ___________
------------------------------------------------------------
"""

import socket
import threading

# ---------------------------------------------------------
# Server Configuration
# ---------------------------------------------------------

HOST = "127.0.0.1"      # Change to your LAN IP for network testing
PORT = 5000
BUFFER_SIZE = 1024

# ---------------------------------------------------------
# Create Server Socket
# ---------------------------------------------------------

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))

server.listen(10)

print("=" * 60)
print("        TCP SELECTIVE GROUP CHAT SERVER")
print("=" * 60)
print(f"Server Running at {HOST}:{PORT}")
print("Waiting for clients...\n")

# ---------------------------------------------------------
# Global Variables
# ---------------------------------------------------------

# username -> socket object
clients = {}

# socket -> username
client_names = {}

lock = threading.Lock()

# ---------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------

def send_message(client_socket, message):
    """
    Send a message to one client.
    """

    try:
        client_socket.send(message.encode())

    except:
        pass


# ---------------------------------------------------------

def send_user_list():
    """
    Sends updated online user list to all clients.

    Protocol:
        USERS|Alice,Bob,Charlie
    """

    with lock:

        user_list = ",".join(clients.keys())

        packet = f"USERS|{user_list}"

        for sock in clients.values():

            try:
                sock.send(packet.encode())

            except:
                pass


# ---------------------------------------------------------

def notify_join(username):
    """
    Notify every client that a user joined.
    """

    packet = f"INFO|{username} joined the chat."

    with lock:

        for sock in clients.values():

            try:
                sock.send(packet.encode())

            except:
                pass


# ---------------------------------------------------------

def notify_leave(username):
    """
    Notify every client that a user left.
    """

    packet = f"INFO|{username} left the chat."

    with lock:

        for sock in clients.values():

            try:
                sock.send(packet.encode())

            except:
                pass


# ---------------------------------------------------------

def remove_client(client_socket):
    """
    Remove disconnected client from server.
    """

    with lock:

        if client_socket not in client_names:
            return

        username = client_names[client_socket]

        print(f"{username} disconnected.")

        del client_names[client_socket]

        if username in clients:
            del clients[username]

    notify_leave(username)

    send_user_list()

    try:
        client_socket.close()
    except:
        pass


# ---------------------------------------------------------

def route_message(sender, receivers, message):
    """
    Send message only to selected users.

    receivers -> list of usernames
    """

    delivered = []
    invalid = []

    with lock:

        for user in receivers:

            user = user.strip()

            if user in clients:

                try:

                    packet = f"MSG|{sender}|{message}"

                    clients[user].send(packet.encode())

                    delivered.append(user)

                except:

                    invalid.append(user)

            else:

                invalid.append(user)

        # Send delivery report back to sender

        if sender in clients:

            sender_socket = clients[sender]

            if delivered:

                sender_socket.send(
                    f"INFO|Delivered to : {', '.join(delivered)}".encode()
                )

            if invalid:

                sender_socket.send(
                    f"ERROR|User(s) Offline : {', '.join(invalid)}".encode()
                )


# ---------------------------------------------------------
# End of Part 1
# ---------------------------------------------------------
# ---------------------------------------------------------
# Client Handler
# ---------------------------------------------------------

def handle_client(client_socket):
    """
    Handles communication with one client.

    Protocol

    LOGIN|username

    SEND|sender|receiver1,receiver2|message

    EXIT|username
    """

    username = ""

    try:

        # -------------------------------
        # Receive Login Packet
        # -------------------------------

        packet = client_socket.recv(BUFFER_SIZE).decode()

        if not packet.startswith("LOGIN|"):
            client_socket.send("ERROR|Invalid Login".encode())
            client_socket.close()
            return

        username = packet.split("|")[1].strip()

        # -------------------------------
        # Username Validation
        # -------------------------------

        with lock:

            if username in clients:

                client_socket.send(
                    "ERROR|Username already exists.".encode()
                )

                client_socket.close()
                return

            clients[username] = client_socket
            client_names[client_socket] = username

        print(f"{username} joined the chat.")

        client_socket.send(
            "INFO|Login Successful".encode()
        )

        notify_join(username)

        send_user_list()

        # -------------------------------
        # Receive Messages
        # -------------------------------

        while True:

            packet = client_socket.recv(BUFFER_SIZE).decode()

            if not packet:
                break

            parts = packet.split("|", 3)

            command = parts[0]

            # -------------------------------
            # SEND Message
            # -------------------------------

            if command == "SEND":

                if len(parts) != 4:

                    send_message(
                        client_socket,
                        "ERROR|Invalid Packet"
                    )

                    continue

                sender = parts[1]

                receivers = parts[2].split(",")

                message = parts[3]

                print()

                print("--------------------------------")

                print("From      :", sender)

                print("To        :", ", ".join(receivers))

                print("Message   :", message)

                print("--------------------------------")

                route_message(
                    sender,
                    receivers,
                    message
                )

            # -------------------------------
            # EXIT
            # -------------------------------

            elif command == "EXIT":

                break

            # -------------------------------
            # Unknown Command
            # -------------------------------

            else:

                send_message(
                    client_socket,
                    "ERROR|Unknown Command"
                )

    except Exception as e:

        print(f"Connection Lost : {username}")

    finally:

        remove_client(client_socket)
# ---------------------------------------------------------
# Accept Client Connections
# ---------------------------------------------------------

def accept_clients():
    """
    Accept new client connections and create
    a separate thread for each client.
    """

    while True:

        try:

            client_socket, address = server.accept()

            print(f"\nNew Connection : {address}")

            thread = threading.Thread(
                target=handle_client,
                args=(client_socket,)
            )

            thread.daemon = True
            thread.start()

        except OSError:
            # Server socket has been closed
            break

        except Exception as e:
            print("Accept Error :", e)


# ---------------------------------------------------------
# Server Administrator Commands
# ---------------------------------------------------------

def server_console():
    """
    Administrator console.

    Commands

    users   -> Display online users
    exit    -> Shutdown server (only if no clients connected)
    help    -> Display available commands
    """

    while True:

        command = input("\nSERVER> ").strip().lower()

        # -----------------------------------

        if command == "users":

            with lock:

                print("\nOnline Users")

                print("-" * 30)

                if len(clients) == 0:
                    print("No users online.")

                else:

                    count = 1

                    for user in clients.keys():
                        print(f"{count}. {user}")
                        count += 1

        # -----------------------------------

        elif command == "help":

            print("\nAvailable Commands")

            print("----------------------")
            print("users  -> Show online users")
            print("help   -> Display commands")
            print("exit   -> Shutdown server")

        # -----------------------------------

        elif command == "exit":

            with lock:

                if len(clients) != 0:

                    print("\nCannot shutdown server.")

                    print(
                        f"{len(clients)} client(s) still connected."
                    )

                    continue

            print("\nShutting down server...")

            try:
                server.close()
            except:
                pass

            break

        # -----------------------------------

        else:

            print("Unknown Command.")

            print("Type 'help' for available commands.")


# ---------------------------------------------------------
# Main Function
# ---------------------------------------------------------

def main():

    print("=" * 60)
    print("      TCP SELECTIVE GROUP CHAT SERVER")
    print("=" * 60)

    print(f"Listening on {HOST}:{PORT}")

    print("\nAdministrator Commands")

    print("--------------------------")
    print("help")
    print("users")
    print("exit")

    print()

    # Thread to accept clients
    accept_thread = threading.Thread(
        target=accept_clients
    )

    accept_thread.daemon = True
    accept_thread.start()

    # Main thread becomes admin console
    server_console()

    accept_thread.join()

    print("\nServer stopped successfully.")


# ---------------------------------------------------------

if __name__ == "__main__":
    main()
