import socket
import math

HOST = ''  # Empty string means to listen on all available interfaces
PORT = 12345  # Port to bind to

# Function to perform arithmetic operations
def calc(a, op, b=None):
    try:
        if op == "+":
            return a + b
        elif op == "-":
            return a - b
        elif op == "*":
            return a * b
        elif op == "/":
            return a / b
        elif op == "%":
            return a % b
        elif op == "sqrt":
            return math.sqrt(a)
        elif op == "^":
            return math.pow(a,b)
        elif op == "log":
            return math.log(a)  # Natural logarithm
        elif op == "sin":
            return math.sin(math.radians(a))  # Convert to radians
        elif op == "cos":
            return math.cos(math.radians(a))  # Convert to radians
        elif op == "tan":
            return math.tan(math.radians(a))  # Convert to radians
        else:
            return "Invalid symbol"
    except ValueError:
        return "Value Error"
    except ZeroDivisionError:
        return "Zero Division Error"
    except Exception as e:
        return str(e)  # Handle any other unexpected errors

# Main server function
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))  # Bind to the specified HOST and PORT
    server_socket.listen()  # Start listening for connections
    print(f"Server is listening on port {PORT}...")

    while True:
        # Accept a new connection from a client
        conn, addr = server_socket.accept()
        print(f"Connected by {addr}")
        with conn:
            while True:
                data = conn.recv(1024)  # Receive data from the client
                if not data:
                    # Break if no data is received (client has disconnected)
                    print(f"Client {addr} has disconnected.")
                    break
                # Split and decode the received data
                try:
                    parts = data.decode().split()
                    if len(parts) == 3:
                        a, b, op = parts
                        a = int(a)
                        b = int(b)
                    elif len(parts) == 2:
                        a, op = parts
                        a = int(a)
                        b = None  # No second operand for unary operations
                    else:
                        raise ValueError("Invalid input format")

                    print(f"Received: {a} {op} {b if b is not None else ''}")

                    # Perform the calculation and send the result back to the client
                    res = str(calc(a, op, b))
                except (ValueError, IndexError):
                    res = "Error: Invalid input format"
                
                conn.sendall(res.encode())  # Send the result back to the client
