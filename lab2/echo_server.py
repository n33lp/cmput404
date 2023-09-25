import socket
from threading import Thread

'''It listens on a specified IP address and port, accepts incoming connections, and then echoes back any data it receives from clients. '''


BYTES_TO_READ = 4096
HOST = "127.0.0.1"  # Local host IP address
PORT = 8000

# Function to handle a single client connection and echo received data
def handle_connection(conn, addr):
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(BYTES_TO_READ)
            if not data:
                break
            print(data)
            conn.sendall(data)  # Echo the received data back to the client

# Function to start the echo server (single-threaded)
def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.listen()
        conn, addr = s.accept()
        handle_connection(conn, addr)

# Function to start the echo server (multi-threaded)
def start_threaded_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.listen(2)  # Listen for up to 2 incoming connections
        
        while True:
            conn, addr = s.accept()
            # Create a new thread to handle each incoming connection
            thread = Thread(target=handle_connection, args=(conn, addr))
            thread.start()  # Start the thread to handle the connection

# Start the multi-threaded echo server
start_threaded_server()
