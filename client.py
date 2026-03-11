import socket
import threading
from Crypto.Cipher import AES

SERVER = "127.0.0.1"
PORT = 5555
KEY = b'ThisIsASecretKey'

def encrypt_message(message):
    cipher = AES.new(KEY, AES.MODE_CFB)
    ciphertext = cipher.encrypt(message.encode())
    return cipher.iv + ciphertext

def decrypt_message(data):
    iv = data[:16]
    ciphertext = data[16:]
    cipher = AES.new(KEY, AES.MODE_CFB, iv=iv)
    return cipher.decrypt(ciphertext).decode()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect((SERVER, PORT))
    print("Connected to server. Start typing messages.")
except:
    print("Could not connect to server.")
    exit()

def receive():
    while True:
        try:
            data = client.recv(1024)
            if not data:
                break
            message = decrypt_message(data)
            print("\nMessage:", message)
        except:
            break

def write():
    while True:
        msg = input("")
        encrypted = encrypt_message(msg)
        client.send(encrypted)

threading.Thread(target=receive, daemon=True).start()
write()