import socket
import threading

HOST = '127.0.0.1'
PORT = 5000

# Lists to store connected clients and their names
clients = []
names = []

# Create TCP Server Socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("=" * 50)
print("      TCP Multi-Client Chat Server")
print("=" * 50)
print(f"Server started at {HOST}:{PORT}")
print("Type 'exit' to stop the server (only when no clients are connected).\\n")


# ---------------------------------------------------
# Broadcast a message to all connected clients
# ---------------------------------------------------
def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except:
            pass


# ---------------------------------------------------
# Handle communication with a client
# ---------------------------------------------------
def handle(client):

    while True:

        try:
            message = client.recv(1024)

            if not message:
                raise Exception

            broadcast(message)

        except:

            if client in clients:

                index = clients.index(client)

                name = names[index]

                clients.remove(client)
                names.remove(name)

                client.close()

                print(f"{name} disconnected.")

                broadcast(f"{name} left the chat.".encode())

            break


# ---------------------------------------------------
# Accept new client connections
# ---------------------------------------------------
def receive():

    while True:

        try:

            client, address = server.accept()

            print(f"Connected : {address}")

            client.send("NAME".encode())

            name = client.recv(1024).decode()

            names.append(name)
            clients.append(client)

            print(f"{name} joined the chat.")

            broadcast(f"{name} joined the chat.".encode())

            thread = threading.Thread(target=handle, args=(client,))
            thread.start()

        except OSError:
            # Happens when server socket is closed
            break


# ---------------------------------------------------
# Listen for server administrator commands
# ---------------------------------------------------
def server_commands():

    while True:

        command = input()

        if command.lower() == "exit":

            if len(clients) == 0:

                print("\\nNo active clients.")
                print("Stopping server...")

                server.close()

                break

            else:

                print("\\nCannot stop the server.")
                print("Active Clients :", len(clients))

                print("Disconnect all clients before exiting.\\n")


# ---------------------------------------------------
# Start Threads
# ---------------------------------------------------

receive_thread = threading.Thread(target=receive)
receive_thread.start()

command_thread = threading.Thread(target=server_commands)
command_thread.start()

# Wait for both threads to finish
receive_thread.join()
command_thread.join()

print("\\nServer terminated successfully.")
