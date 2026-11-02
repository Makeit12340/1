import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 5000))

print("Connected to server:", client_socket.getpeername())
print("Client address:", client_socket.getsockname())

while True:
    message = input("Enter message (type 'exit' to quit): ")
    if message.lower() == 'exit':
        break

    client_socket.send(message.encode())
    data = client_socket.recv(1024)
    print("Echo from Server:", data.decode())

client_socket.close()
