import socket
import threading #many threads running

#if use online put private ip address here
#if use online ip need to open port
HOST = "127.0.0.1"
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()
clients = []
nicknames = []

#broadcast function
def broadcast(message):
    for client in clients:
        client.send(message)

#recieve
def receive():
    while True:
        client,address =  server.accept()
        #print to server
        print(f"You are connected with {str(address)}!")

        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024)

        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}")
        broadcast(f"{nickname} is now connected!\n".encode('utf-8'))
        client.send("Connected to the server".encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))#treat the client as tuple
        thread.start()

#handle
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{nicknames[clients.index(client)]} says {message}") #print on the server
            broadcast(message)
        except:
            index =  clients.index(client)
            nicknames.remove(nicknames[index])
            clients.remove(client)
            client.close()
            break
print("Server running")
receive()
