import socket
import threading
import ssl

# Sets the server address from local host
server_address = 'localhost'
# Get the server port from the user
server_port = int(input("Enter the server port (default is 9000): ") or 9000)

# Create a place to store connected clients and their usernames
clients = {}


# Function to handle a client's connection
def handle_client(current_socket, current_client_ssl):
    # Ask the client to provide a username
    username = current_client_ssl.recv(1024).decode().strip()

    # Check if the username is unique
    for sock, ssl_and_username in clients.items():
        if username == ssl_and_username[0]:
            current_client_ssl.send("Username already taken. Please choose another one.".encode())
            handle_client(current_socket,current_client_ssl)

    clients[current_socket] = [username, current_client_ssl]
    print(f"Client connected with username: {username}")

    # Notify all clients about the new user
    for sock, ssl_and_username in clients.items():
        if ssl_and_username[0] != username:
            ssl_and_username[1].send(f"{username} has joined the chat.".encode())

    current_client_ssl.send(f"Instructions:\n" f"Use @ then the name of the user followed by your message".encode())

    if len(clients) > 1:
        current_client_ssl.send(f"Here's a list of users online right now: ".encode())
        for sock, ssl_and_username in clients.items():
            if ssl_and_username[0] != username:
                current_client_ssl.send(f"{ssl_and_username[0]}".encode())
    else:
        current_client_ssl.send(f"Waiting for another user to join".encode())

    try:
        while True:
            message = current_client_ssl.recv(1024).decode()
            if not message:
                break

            if message.startswith("@"):
                recipient, private_message = message.split(" ", 1)
                recipient = recipient[1:]

                for sock, ssl_and_username in clients.items():
                    if ssl_and_username[0] == recipient:
                        ssl_and_username[1].send(f"{username} says: {private_message}".encode())

            else:
                current_client_ssl.send(f"Use @ followed by username of person to send message. eg @user1 some "
                                        f"message".encode())

    finally:
        print(f"Client {username} has disconnected.")
        del clients[current_socket]
        current_client_ssl.close()


context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain(certfile="server-cert.pem", keyfile="server-key.pem")

# Start the server
# Create a socket for the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_address, server_port))
server_socket.listen(5)
print(f"Server is listening on {server_address}:{server_port} for incoming connections...")

while True:
    client_socket, client_address = server_socket.accept()
    client_ssl = context.wrap_socket(client_socket, server_side=True)
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_ssl))
    client_thread.start()
