from flask import Flask, render_template, request
import socket

app = Flask(__name__)

# TCP client function
def arithmetic_client_tcp(server_addr, number1, number2, operation):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(server_addr)
        message = f"{number1} {number2} {operation}"
        print(message)
        client_socket.sendall(message.encode())
        data = client_socket.recv(1024)
        return data.decode()

# UDP client function
def arithmetic_client_udp(server_addr, number1, number2, operation):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = f"{number1} {number2} {operation}"
    print("udp")
    print(message)
    client_socket.sendto(message.encode(), server_addr)
    data, _ = client_socket.recvfrom(1024)
    client_socket.close()
    return data.decode()

# Default route
@app.route('/')
def index():
    return render_template('index.html')

# Route for calculation
@app.route('/calculate', methods=['POST'])
def calculate():
    print("Received calculation request")
    number1 = request.form['num1']
    number2 = request.form['num2']
    operation = request.form['operation']
    protocol = request.form['protocol']

    server_ip = '192.168.100.253'
    server_port = 12345
    server_addr = (server_ip, server_port)

    # Adjust the number of operands based on the operation
    if operation in ['sqrt', 'log', 'sin', 'cos', 'tan']:
        # Send only one operand for unary operations
        response = arithmetic_client_tcp(server_addr, number1, '', operation) if protocol == 'TCP' else arithmetic_client_udp(server_addr, number1, '', operation)
    else:
        # Send both operands for binary operations
        response = arithmetic_client_tcp(server_addr, number1, number2, operation) if protocol == 'TCP' else arithmetic_client_udp(server_addr, number1, number2, operation)

    return render_template('index.html', response=response)

if __name__ == '__main__':
    app.run(debug=True)
