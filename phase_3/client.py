import socket
import threading


class ChatClient:
    def __init__(self, host, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
        self.running = False

    def get_username(self):
        """Get and send username to server"""
        prompt = self.client_socket.recv(1024).decode("utf-8")
        if prompt == "username":
            name = input("Please enter your username: ").strip()
            while not name:
                name = input("Username cannot be empty. Please enter your username: ").strip()
            self.client_socket.send(name.encode("utf-8"))
            print(f"\nConnected to server as '{name}'. Type /exit to quit.\n")

    def receive_messages(self):
        """Receive and display messages from server"""
        while self.running:
            try:
                message = self.client_socket.recv(1024).decode("utf-8")
                if not message:
                    break
                print(message)
            except:
                print("\nDisconnected from server.")
                self.running = False
                break

    def send_messages(self):
        """Send messages to server"""
        while self.running:
            try:
                message = input()
                if not self.running:
                    break
                if message.lower() == "/exit":
                    self.client_socket.close()
                    self.running = False
                    break
                self.client_socket.send(message.encode("utf-8"))
            except:
                self.running = False
                break

    def start(self):
        """Start the client"""
        self.running = True
        self.get_username()

        receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
        send_thread = threading.Thread(target=self.send_messages, daemon=True)

        receive_thread.start()
        send_thread.start()

        try:
            while self.running:
                if not receive_thread.is_alive() or not send_thread.is_alive():
                    self.running = False
        except KeyboardInterrupt:
            print("\nDisconnecting...")
            self.client_socket.close()
            self.running = False


if __name__ == "__main__":
    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 12345
    client = ChatClient(HOST, PORT)
    client.start()