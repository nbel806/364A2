import socket
import threading

# Create a socket for the client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Sets the server address from local host
server_address = 'localhost'
server_port = int(input("Enter the server port (default is 9000): ") or 9000)

# Connect to the server
client_socket.connect((server_address, server_port))


# Function to receive and display messages from the server
def receive_messages():
    while True:
        message = client_socket.recv(1024).decode()
        print(message)


# Start a thread to receive and display messages
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Ask the user to provide a username
username = input("Please enter your username: ")
client_socket.send(username.encode())


# Function to send messages to the server
def send_messages():
    while True:
        message = input()
        client_socket.send(message.encode())


# Start a thread to send messages
send_thread = threading.Thread(target=send_messages)
send_thread.start()
