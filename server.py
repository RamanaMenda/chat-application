import socket
import threading

HOST = 'localhost'
PORT = 45555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server.bind((HOST, PORT))
except socket.error as e:
    print(str(e))

server.listen()

clients, names = [], []

def broadcast(msg):
    for client in clients:
        client.send(msg)

def handle(client):
    while True:
        try:
            msg = client.recv(1024)
            if not msg:
                raise Exception("Client disconnected.")
            print(f'{names[clients.index(client)].decode()} has sent a msg')
            broadcast(msg)
        except:
            target_index = clients.index(client)
            clients.remove(client)
            client.close()
            rname = names[target_index]
            names.remove(rname)
            broadcast(f"{rname.decode()} left the chat \n".encode('utf-8'))
            break

def receive():
    while True:
        try:
            client, address = server.accept()
            print(f"connected with {address[0]} : {address[1]}!")

            client.send('NAME:'.encode('utf-8'))
            name = client.recv(1024).decode()

            if not name: 
                client.close()
                continue

            names.append(name.encode('utf-8'))
            clients.append(client)

            print(f"{name} connected to the server")

            broadcast(f"{name} joined the chat \n".encode('utf-8'))
            client.send('connected to the chat'.encode('utf-8'))

            thread = threading.Thread(target=handle, args=(client,))
            thread.start()

        except socket.error as e:
            print(f"Socket error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")


print('--->  WAITING FOR CONNECTIONS.....')
try:
    receive()
except KeyboardInterrupt:
    server.close()
    print("Server closed!")
