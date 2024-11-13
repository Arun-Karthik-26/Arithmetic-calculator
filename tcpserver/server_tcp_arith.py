import socket
import math


# Function to perform arithmetic operations
def calc(a, op, b=None):
    try:
        a = float(a)  # Convert a to float to handle non-integer input
        if b is not None:
            b = float(b)  # Convert b to float if it's provided
        if op == "+":
            return a + b
        elif op == "-":
            return a - b
        elif op == "*":
            return a * b
        elif op == "/":
            return a / b if b != 0 else "Error: Division by zero"
        elif op == "%":
            return a % b
        elif op == "sqrt":
            return math.sqrt(a)
        elif op == "^":
            return math.pow(a, b)
        elif op == "log":
            return math.log(a)  # Natural logarithm
        elif op == "sin":
            return math.sin(math.radians(a))  # Convert to radians
        elif op == "cos":
            return math.cos(math.radians(a))  # Convert to radians
        elif op == "tan":
            return math.tan(math.radians(a))  # Convert to radians
        else:
            return "Error: Invalid operation"
    except ValueError:
        return "Error: Value error"
    except ZeroDivisionError:
        return "Error: Division by zero"
    except Exception as e:
        return f"Error: {str(e)}"  # Handle any other unexpected errors

# Main server function
def start_server():
    HOST = '0.0.0.0'  # Listen on all available interfaces
    PORT = 12345  # Default port to 12345 if not set

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))  # Bind to the specified HOST and PORT
        server_socket.listen()  # Start listening for connections
        print(f"Server is listening on {HOST}:{PORT}...")

        while True:
            # Accept a new connection from a client
            conn, addr = server_socket.accept()
            print(f"Connected by {addr}")
            with conn:
                while True:
                    try:
                        data = conn.recv(1024)  # Receive data from the client
                        if not data:
                            # Break if no data is received (client has disconnected)
                            print(f"Client {addr} has disconnected.")
                            break

                        # Split and decode the received data
                        parts = data.decode().split()
                        if len(parts) == 3:
                            a, b, op = parts
                            res = calc(a, op, b)
                        elif len(parts) == 2:
                            a, op = parts
                            res = calc(a, op)
                        else:
                            res = "Error: Invalid input format"

                        print(f"Received: {data.decode()} -> Result: {res}")
                        conn.sendall(str(res).encode())  # Send the result back to the client

                    except Exception as e:
                        print(f"Error handling client {addr}: {str(e)}")
                        conn.sendall("Error: Unable to process request".encode())
                        break

if __name__ == "__main__":
    start_server()
