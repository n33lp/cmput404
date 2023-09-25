import socket
''' 
This code sends HTTP GET requests to both "www.google.com" and "localhost" on the specified ports and prints the responses received from those servers.
'''
BYTES_TO_READ = 4096

# Function to send an HTTP GET request to a specified host and port
def get(host, port):
    # Define the HTTP GET request with the provided host and port
    request = b"GET / HTTP/1.1\nHost: " + host.encode('utf-8') + b"\n\n"

    # Create a socket connection to the target host and port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))  # Connect to the target host and port

    # Send the HTTP GET request to the target server
    s.send(request)

    # Shutdown the write end of the socket to signal that we've finished sending
    s.shutdown(socket.SHUT_WR)

    # Receive and print the response data in chunks until there's no more data
    result = s.recv(BYTES_TO_READ)
    while len(result) > 0:
        print(result)
        result = s.recv(BYTES_TO_READ)

    # Close the socket connection
    s.close()

# Call the get() function to send an HTTP GET request to the specified hosts and ports
get("www.google.com", 80)
get("localhost", 8080)
