import socket
import threading


class ChatServer:
    def __init__(self, host, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen()
        self.clients = {}
        print(f"\n{'*' * 30}")
        print("Server is running and waiting for connections...")
        print(f"{'*' * 30}\n")

    def broadcast(self, message, sender=None):
        """Send message to all clients except the sender"""
        for client_socket in self.clients.keys():
            if client_socket != sender:
                try:
                    client_socket.send(message.encode("utf-8"))
                except:
                    self.remove_client(client_socket)

    def remove_client(self, client_socket):
        """Remove a client from the server"""
        if client_socket in self.clients:
            name = self.clients[client_socket]
            address = client_socket.getpeername()
            del self.clients[client_socket]
            client_socket.close()
            leave_msg = f"\033[1;31m\n\t{name} ({address[0]}:{address[1]}) has left the server!\n\033[0m"
            self.broadcast(leave_msg)
            print(f"{name} ({address[0]}:{address[1]}) has left the server.")
            print(f"{'*' * 30}")

    def handle_client(self, client_socket):
        """Handle communication with a client"""
        try:
            # Get client name
            client_socket.send("username".encode('utf-8'))
            client_name = client_socket.recv(1024).decode('utf-8').strip()

            if not client_name:
                raise ValueError("Empty username")

            address = client_socket.getpeername()
            self.clients[client_socket] = client_name
            print(f"Client: {client_name} ({address[0]}:{address[1]})")
            print(f"{'*' * 30}")

            welcome_msg = f"\nWelcome {client_name}, you are connected to the server.\n"
            client_socket.send(welcome_msg.encode('utf-8'))

            join_msg = f"\033[1;92m\n{client_name} has joined the server.\n\033[0m"
            self.broadcast(join_msg, client_socket)

            # Handle messages from client
            while True:
                message = client_socket.recv(1024).decode("utf-8")
                if not message or message.lower() == "/exit":
                    raise Exception("Client disconnected")

                formatted_msg = f"\033[1;34m\n\t{client_name} ({address[0]}:{address[1]}): {message}\n\033[0m"
                self.broadcast(formatted_msg, client_socket)

        except Exception as e:
            self.remove_client(client_socket)

    def start(self):
        """Start accepting client connections"""
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"New connection from {client_address[0]}:{client_address[1]}")
            print(f"{'*' * 30}")

            client_thread = threading.Thread(
                target=self.handle_client,
                args=(client_socket,),
                daemon=True
            )
            client_thread.start()


if __name__ == "__main__":
    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 12345
    server = ChatServer(HOST, PORT)
    server.start()