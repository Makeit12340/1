import socket
from urllib.parse import urlparse, parse_qs
from datetime import datetime

HOST = "127.0.0.1"
PORT = 8080

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

print(f"Dynamic HTTP Server running at http://{HOST}:{PORT}")

while True:
    client, address = server.accept()

    request = client.recv(4096).decode()
    print("=" * 60)
    print(request)

    first_line = request.split("\r\n")[0]
    path = first_line.split()[1]

    parsed = urlparse(path)
    route = parsed.path
    params = parse_qs(parsed.query)

    if route == "/":
        html = f"""
        <html>
        <h1>Computer Network Lab</h1>
        <p>Dynamic HTTP Server</p>
        <p>Current Time:</p>
        {datetime.now()}
        </html>
        """

    elif route == "/student":
        name = params.get("name", ["Student"])[0]
        html = f"""
        <html>
        <h1>Welcome {name}</h1>
        <h2>Computer Networks Lab</h2>
        </html>
        """

    elif route == "/add":
        try:
            a = int(params.get("a", [0])[0])
            b = int(params.get("b", [0])[0])
            html = f"""
            <html>
            <h1>Addition Result</h1>
            <h2>{a} + {b} = {a + b}</h2>
            </html>
            """
        except (ValueError, TypeError):
            html = "<html><h2>Invalid Number</h2></html>"

    elif route == "/time":
        html = f"""
        <html>
        <h1>Current Server Time</h1>
        <h2>{datetime.now()}</h2>
        </html>
        """

    else:
        html = """
        <html>
        <h1>404 Not Found</h1>
        </html>
        """

    status = "404 Not Found" if route not in ("/", "/student", "/add", "/time") else "200 OK"
    body = html.encode()

    response = (
        f"HTTP/1.1 {status}\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(body)}\r\n"
        "Connection: close\r\n"
        "\r\n"
    ).encode() + body

    client.sendall(response)
    client.close()
