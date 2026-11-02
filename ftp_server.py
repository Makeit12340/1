import socket

HOST = "127.0.0.1"
PORT = 5000
BUFFER_SIZE = 4096

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("Waiting for client...")

client, address = server.accept()
print("Connected to:", address)

filename = client.recv(1024).decode()

print("Receiving file:", filename)
file = open("Received_" + filename, "wb")

while True:
    data = client.recv(BUFFER_SIZE)
    if not data:
        break

    file.write(data)

file.close()

print("File received successfully!")

client.close()
server.close()
