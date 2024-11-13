import socket
import math

HOST = ''  # Listen on all available interfaces
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
            return "Invalid symbol cannot find symbol"
    except ValueError:
        return "Value Error"
    except ZeroDivisionError:
        return "Zero Division Error"
    except Exception as e:
        return str(e)  # Handle any other unexpected errors

# Main server function
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
    server_socket.bind((HOST, PORT))  # Bind to the specified HOST and PORT
    print(f"Server is listening on port {PORT}....")

    while True:
        data, addr = server_socket.recvfrom(1024)  # Receive data from the client
        parts = data.decode().split()
        try:
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

        server_socket.sendto(res.encode(), addr)  # Send the result back to the client
