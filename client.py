import socket
import ssl
import threading

# Sets the server address from local host
server_address = 'localhost'
server_port = int(input("Enter the server port (default is 9000): ") or 9000)

context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

# Connect to the server
# Create a socket for the client
client_ssl = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_ssl.connect((server_address, server_port))
client_ssl = context.wrap_socket(client_ssl, server_hostname=server_address)


# Function to receive and display messages from the server
def receive_messages():
    while True:
        message = client_ssl.recv(1024).decode()
        print(message)


# Start a thread to receive and display messages
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Ask the user to provide a username
username = input("Please enter your username: ")
client_ssl.send(username.encode())


# Function to send messages to the server
def send_messages():
    while True:
        message = input()
        client_ssl.send(message.encode())


# Start a thread to send messages
send_thread = threading.Thread(target=send_messages)
send_thread.start()
