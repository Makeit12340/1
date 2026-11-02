import socket
import os

HOST = "127.0.0.1"
PORT = 5000
BUFFER_SIZE = 4096

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((HOST, PORT))

filepath = input("Enter complete file path: ")

if not os.path.isfile(filepath):
    print("File does not exist!")
    client.close()
    exit()

filename = os.path.basename(filepath)
client.send(filename.encode())

with open(filepath, "rb") as file:
    while True:
        data = file.read(BUFFER_SIZE)
        if not data:
            break

        client.send(data)

client.close()

print("File Transfer successful!")
