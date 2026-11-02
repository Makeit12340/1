import socket

HOST = "127.0.0.1"
PORT = 8080

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

request = (
    "GET / HTTP/1.1\r\n"
    f"Host: {HOST}\r\n"
    "Connection: close\r\n"
    "\r\n"
)

client.send(request.encode())

response = b""

while True:
    data = client.recv(4096)
    if not data:
        break
    response += data

print("=" * 60)
print("HTTP RESPONSE")
print("=" * 60)
print(response.decode())

client.close()
