import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 5000))
server_socket.listen(1)

print("Server is waiting for connection")
client_socket, client_address = server_socket.accept()
print("Connected to:", client_address)

while True:
    data = client_socket.recv(1024)
    if not data:
        break

    expression = data.decode()
    print("Client:", expression)

    try:
        parts = expression.split()
        num1 = float(parts[0])
        operator = parts[1]
        num2 = float(parts[2])

        if operator == "+":
            result = num1 + num2
        elif operator == "-":
            result = num1 - num2
        elif operator == "*":
            result = num1 * num2
        elif operator == "/":
            if num2 == 0:
                result = "Cannot divide by zero"
            else:
                result = num1 / num2
        else:
            result = "Invalid operator"

    except:
        result = "Invalid expression"

    client_socket.send(str(result).encode())

client_socket.close()
server_socket.close()
