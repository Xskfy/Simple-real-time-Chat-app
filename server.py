import socket
import threading

def handle_client(client_socket, address, clients):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            message = f"[{address[0]}:{address[1]}] {data.decode('utf-8')}"
            print(message)
            broadcast(message, clients)
            if data.decode('utf-8') == "/quit":
                remove_client(client_socket, clients)
                break
        except Exception as e:
            print(f"Error: {e}")
            break

def broadcast(message, clients):
    for client in clients:
        client.send(message.encode('utf-8'))

def remove_client(client_socket, clients):
    if client_socket in clients:
        clients.remove(client_socket)
        print("Client disconnected")

clients = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 5555))
server.listen(5)

print("Server listening on port 5555")

while True:
    client, address = server.accept()
    print(f"Accepted connection from {address}")
    clients.append(client)
    client_handler = threading.Thread(target=handle_client, args=(client, address, clients))
    client_handler.start()
