import socket
from threading import Thread

# Constants
BYTES_TO_READ = 4096
PROXY_SERVER_HOST = "127.0.0.1"
PROXY_SERVER_PORT = 8080

# Function to send an HTTP request to the destination server
def send_request(host, port, request):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        client_socket.send(request)
        client_socket.shutdown(socket.SHUT_WR)

        data = client_socket.recv(BYTES_TO_READ)
        result = b'' + data
        while len(data) > 0:
            data = client_socket.recv(BYTES_TO_READ)
            result += data
        return result

# Function to handle a single client connection
def handle_connection(conn, addr):
    with conn:
        print(f"Connected by {addr}")

        request = b''
        while True:
            data = conn.recv(BYTES_TO_READ)
            if not data:
                break
            print(data)
            request += data
        
        # Send the received request to the destination server (e.g., www.google.com)
        response = send_request("www.google.com", 80, request)
        
        # Send the response from the destination server back to the client
        conn.sendall(response)

# Function to start the proxy server (single-threaded)
def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((PROXY_SERVER_HOST, PROXY_SERVER_PORT))

        # Allow reusing the same address and port
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        server_socket.listen(2)  # Listen for incoming connections, queue up to 2
        
        # Accept a single connection and handle it
        conn, addr = server_socket.accept()
        handle_connection(conn, addr)

# Function to start the proxy server (multi-threaded)
def start_threaded_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((PROXY_SERVER_HOST, PROXY_SERVER_PORT))
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        server_socket.listen(2)  # Listen for incoming connections, queue up to 2

        while True:
            conn, addr = server_socket.accept()
            # Create a new thread to handle each incoming connection
            thread = Thread(target=handle_connection, args=(conn, addr))
            thread.start()  # Start the thread to handle the connection

# Uncomment start_server() or start_threaded_server() to choose the server mode.
# start_server()  # for a single-threaded proxy server
start_threaded_server()  # for a multi-threaded proxy server



# Single-Threaded Server:
# In a single-threaded server, there is only one main thread that accepts incoming client connections and handles them one at a time sequentially.
# When a client connects, the server accepts the connection and processes the client's request. During this time, the server cannot accept new connections until it finishes handling the current one.
# This mode is simpler to implement and understand but can handle only one connection at a time. If multiple clients connect simultaneously, they will be processed one after the other, potentially leading to slower response times for clients.


# Multi-Threaded Server:
# In a multi-threaded server, multiple threads are used to handle incoming client connections concurrently. Each incoming connection is assigned to a separate thread, allowing multiple clients to be served simultaneously.
# When a client connects, the server creates a new thread to handle that client's request independently. This means that other clients can still connect and be served by their respective threads.
# Multi-threaded servers can handle multiple connections concurrently, making them more efficient and responsive, especially when dealing with a high number of clients. However, they require careful synchronization to avoid data races and thread-related issues.