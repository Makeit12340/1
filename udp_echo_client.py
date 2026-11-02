import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('127.0.0.1', 5000)

print("UDP Echo Client Started")

while True:
    message = input("\nEnter message (type 'exit' to quit): ")
    client_socket.sendto(message.encode(), server_address)
    print("Client Address:", client_socket.getsockname())

    if message.lower() == 'exit':
        break

    data, server = client_socket.recvfrom(1024)
    print("Echo from Server:", data.decode())

client_socket.close()
