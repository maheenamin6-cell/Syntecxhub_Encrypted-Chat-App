import socket
import threading
from Crypto.Cipher import AES

SERVER = "127.0.0.1"
PORT = 5555
KEY = b'ThisIsASecretKey'

name = input("Enter your name: ")

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
client.connect((SERVER, PORT))

def receive():
    while True:
        try:
            data = client.recv(1024)
            message = decrypt_message(data)
            print(message)
        except:
            break

def write():
    while True:
        msg = input("")
        full_message = f"{name}: {msg}"
        encrypted = encrypt_message(full_message)
        client.send(encrypted)

threading.Thread(target=receive).start()
write()