import socket
from threading import Thread

def recv_message(sock):
    while True:
        msg = sock.recv(1024)
        print(msg.decode())

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 8274))

thr = Thread(target = recv_message, args = (sock, ))
thr.daemon = True
thr.start()

while True:
    msg = input()
    sock.send(msg.encode())
    if msg == '/exit':
        break

sock.close()