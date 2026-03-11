import socket
import threading
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from datetime import datetime

HOST = "0.0.0.0"
PORT = 5555

KEY = b'ThisIsASecretKey'  # 16 bytes AES key

clients = []

def encrypt_message(message):
    cipher = AES.new(KEY, AES.MODE_CFB)
    ciphertext = cipher.encrypt(message.encode())
    return cipher.iv + ciphertext

def decrypt_message(data):
    iv = data[:16]
    ciphertext = data[16:]
    cipher = AES.new(KEY, AES.MODE_CFB, iv=iv)
    return cipher.decrypt(ciphertext).decode()

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            client.send(message)

def handle_client(client_socket, addr):
    print(f"[NEW CONNECTION] {addr} connected")
    
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break

            message = decrypt_message(data)

            # log message
            with open("chat_log.txt", "a") as f:
                f.write(f"{message}\n")

            print(f"{addr}: {message}")

            broadcast(data, client_socket)

        except:
            break

    clients.remove(client_socket)
    client_socket.close()
    print(f"[DISCONNECTED] {addr}")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"[SERVER STARTED] Listening on {PORT}")

    while True:
        client_socket, addr = server.accept()
        clients.append(client_socket)

        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

start_server()