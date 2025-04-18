import socket
import threading

#creating the server socket IPV4 (AF_INET) and TCP (SOCK_STREAM)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#bind the sever to your computer ip and a desired port
server_socket.bind((socket.gethostbyname(socket.gethostname()), 12345))

# put it on listen (for incoming connection)
server_socket.listen()

#a dictionary for clients
clients = dict()


def broadcast(message):
    """show the messages for everyone"""
    for client in clients.keys():
        client.send(message)


def receive_message(client_socket):
    """receive message from client"""

    while True:
        address = str(client_socket)[-26:-3]
        # we need a try except so that our program doesn't crash
        try:
            #receive the message from the client
            message = client_socket.recv(1024).decode("utf-8")
            if message.lower() == "/exit":
                raise Exception
            message = f"\033[1;34m\n\t{clients[client_socket]} ({address}): {message}\n\033[0m".encode("utf-8")
            #show the message to everyone
            broadcast(message)
        except:
            #name of client
            name = clients[client_socket]
            #remove the client from the dictionary
            clients.pop(client_socket)
            #close the connection for the client
            client_socket.close()
            #let others know that the client left the server
            broadcast(f"\033[1;31m\n\t{name} ({address}) has left the server!\n\033[0m".encode("utf-8"))
            print(f"{name} ({address}) has left the server.")
            print("*" * 30)
            break


def connect_client():
    """connecting to server"""
    while True:

        #accept incoming connections
        client_socket, client_address = server_socket.accept()
        print(f"{client_address} has connected.")
        print("*" * 30)

        try:

            #request for client name
            client_socket.send(f"username".encode('utf-8'))
            client_name = client_socket.recv(1024).decode('utf-8')

            #adding the client to dictionary
            if len(client_name) != 0:

                clients.update({client_socket: client_name})
                print(f"client: {clients[client_socket]} {str(client_socket)[-27:-1]}")
                print("*" * 30)

                #informing the client
                client_socket.send(f"\nwelcome {clients[client_socket]}, you are connected to the server.\n".encode('utf-8'))
                broadcast(f"\033[1;92m\n{clients[client_socket]} has joined the server.\n\033[0m".encode("utf-8"))
            else:
                raise Exception

        except:

            print(f"({str(client_socket)[-25:-2]}) has left the server.")
            print("*" * 30)
            continue

        #when a client connects to the server stat a thread
        receive_thread = threading.Thread(target=receive_message, args=(client_socket,))
        receive_thread.start()


#set up the server
print()
print("*" * 30)
print("server is looking for connection...")
print("*" * 30)
connect_client()

