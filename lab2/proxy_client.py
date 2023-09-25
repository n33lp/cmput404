import socket

'''
Sends an HTTP GET request to a specified proxy server (in this case, "127.0.0.1" on port 8080). The proxy server is expected to forward the request to the destination server ("www.google.com") and return the response.
'''

BYTES_TO_READ = 4096


# Function to send an HTTP GET request to the proxy server and retrieve the response
def get(host, port):
    # Define the HTTP GET request to be sent to the proxy server
    request = b"GET / HTTP/1.1\nHost: www.google.com\n\n"

    # Create a socket connection to the proxy server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))  # Connect to the proxy server

        # Send the HTTP GET request to the proxy server
        s.send(request)

        # Shutdown the write end of the socket to signal that we've finished sending
        s.shutdown(socket.SHUT_WR)

        # Initialize variables to store the response data
        chunk = s.recv(BYTES_TO_READ)
        result = b'' + chunk

        # Receive and accumulate response data in chunks until there's no more data
        while len(chunk) > 0:
            chunk = s.recv(BYTES_TO_READ)
            result += chunk

        # Close the socket connection
        s.close()

        return result

# Call the get() function to send the request to the proxy server and print the response
print(get("127.0.0.1", 8080))