import socket

HOST = "127.0.0.1"
PORT = 8080

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("Mini HTTP Server Running!")
print(f"Listening on http://{HOST}:{PORT}")

while True:
    client, address = server.accept()
    print("\nConnected:", address)

    request = client.recv(4096).decode()
    print("\nHTTP Request")
    print("-" * 50)
    print(request)

    html = """
    <html>
    <head>
        <title>Computer Network Lab</title>
    </head>
    <body>
        <h1>Mini HTTP Server</h1>
        <h2>Computer Networks Laboratory</h2>
        <p>Hello Student!</p>
        <p>The page is served using Python sockets.</p>
    </body>
    </html>
    """

    response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html\r\n"
        f"Content-Length: {len(html.encode())}\r\n"
        "Connection: close\r\n"
        "\r\n"
        + html
    )

    client.sendall(response.encode())
    client.close()
