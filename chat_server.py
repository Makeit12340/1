import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(('127.0.0.1', 5000))

server_socket.listen()

print("Server is waiting for connection...")

client_socket, client_address = server_socket.accept()

print("Connected to:", client_address)

while True:
    data = client_socket.recv(1024)
    message = data.decode()

    print("Client:", message)

    if message.lower() == "exit":
        break

    reply = input("Server: ")

    client_socket.send(reply.encode())

    if reply.lower() == "exit":
        break

client_socket.close()
server_socket.close()

print("Chat ended")
