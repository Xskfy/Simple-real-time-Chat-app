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
    entry.delete(0, tk.END)  
    if message == "/quit":
        client_socket.close()
        root.destroy()

def on_closing(event=None):
    entry.delete(0, tk.END)
    entry.insert(0, "/quit")
    send()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 5555))


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


receive_thread = threading.Thread(target=receive)
receive_thread.start()

root.mainloop()
