# Simple-real-time-Chat-app

This is a blog site thingy for a school activity. 

I am Jon Angelo T. Abello and this is the Simple Real-time chat app program blog.

The Goal was to use python sockets and tkinter. 

starting it up, was the server script
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

this should handle the server and accept messages broadcasted back to its users (just one for this same device).

next was the client to connect to the server and receive messages from broadcast 

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, Entry, Button

def receive():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            chat_box.insert(tk.END, message + '\n')
        except Exception as e:
            print(f"Error: {e}")
            break

def send(event=None):
    message = entry.get()
    client_socket.send(message.encode('utf-8'))
    if message == "/quit":
        client_socket.close()
        root.destroy()

def on_closing(event=None):
    entry.delete(0, tk.END)
    entry.insert(0, "/quit")
    send()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 5555))

# GUI setup
root = tk.Tk()
root.title("Simple Chat App")

chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=15)
chat_box.pack(padx=10, pady=10)

entry = Entry(root, width=30)
entry.pack(padx=10, pady=10)
entry.bind("<Return>", send)

send_button = Button(root, text="Send", command=send)
send_button.pack(pady=5)

root.protocol("WM_DELETE_WINDOW", on_closing)

# Start a separate thread to handle receiving messages
receive_thread = threading.Thread(target=receive)
receive_thread.start()

root.mainloop()
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
This client script opens a tkinter window with an open box to display all the messages broadcasted with a client's socket ip address. 
it also has its entry field to send messages with a dedicated button to send. 
the sending and receiving of messages is also real-time.

#changes

1st: Close function - I panicked after pressing close and it only having a "/close" on the entry field and message broadcast so I had to close via task manager, close function has been added

2nd: Entry field - The entry field wasn't clearing per message sent, entry.delete(0, tk.END) line added

