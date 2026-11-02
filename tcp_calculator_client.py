import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 5000))

print("Connected to server:", client_socket.getpeername())
print("Client Address:", client_socket.getsockname())
print("Enter expression as: number operator number")

while True:
    expression = input("Enter expression (type 'exit' to quit): ")
    if expression.lower() == 'exit':
        break

    client_socket.send(expression.encode())
    result = client_socket.recv(1024)
    print("Result:", result.decode())

client_socket.close()
