import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('127.0.0.1', 5000))

print("UDP Echo Server is running")
print("Waiting for message\n")

while True:
    data, client_address = server_socket.recvfrom(1024)
    message = data.decode()
    print(f"Received from {client_address}: {message}")

    if message.lower() == 'exit':
        print("Server shutting down")
        break

    server_socket.sendto(data, client_address)

server_socket.close()
