import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect(('127.0.0.1', 5000))

print("Connected to server:", client_socket)
print("Client Address:", client_socket.getsockname())
print("Type 'exit' to quit")

while True:
    message = input("Client: ")
    client_socket.send(message.encode())

    if message.lower() == "exit":
        break

    data = client_socket.recv(1024)
    reply = data.decode()

    print("Server:", reply)

    if reply.lower() == "exit":
        break

client_socket.close()
print("Chat ended")
