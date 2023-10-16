import socket
import threading

# Create a socket for the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Sets the server address from local host
server_address = 'localhost'
# Get the server port from the user
server_port = int(input("Enter the server port (default is 9000): ") or 9000)

# Create a place to store connected clients and their usernames
clients = {}


# Function to handle a client's connection
def handle_client(current_client_socket):
    # Ask the client to provide a username
    current_client_socket.send("Please enter your username: ".encode())
    username = current_client_socket.recv(1024).decode().strip()

    # Check if the username is unique
    if username in clients.values():
        current_client_socket.send("Username already taken. Please choose another one.".encode())
        current_client_socket.close()
        return
    else:
        clients[current_client_socket] = username
        print(f"Client connected with username: {username}")

    # Notify all clients about the new user
    for sock, username1 in clients.items():
        if username1 != username:
            sock.send(f"{username} has joined the chat.".encode())

    current_client_socket.send(f"Instructions:\n" f"Use @ then the name of the user followed by your message".encode())

    if len(clients) > 1:
        current_client_socket.send(f"Here's a list of users online right now \n".encode())
        for sock, username1 in clients.items():
            if username1 != username:
                current_client_socket.send(f"{username1}".encode())
    else:
        current_client_socket.send(f"Waiting for another user to join".encode())



    try:
        while True:
            message = current_client_socket.recv(1024).decode()
            if not message:
                break

            if message.startswith("@"):
                recipient, private_message = message.split(" ", 1)
                recipient = recipient[1:]

                for sock, username in clients.items():
                    if username == recipient:
                        sock.send(f"{clients[current_client_socket]} says: {private_message}".encode())

            else:
                current_client_socket.send(f"Use @ followed by username of person to send message. eg @user1 some "
                                           f"message".encode())

    except:
        pass
    finally:
        print(f"Client {username} has disconnected.")
        del clients[current_client_socket]
        current_client_socket.close()


# Start the server
server_socket.bind((server_address, server_port))
server_socket.listen(5)
print(f"Server is listening on {server_address}:{server_port} for incoming connections...")

while True:
    client_socket, client_address = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
