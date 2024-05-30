import socket
from threading import Thread
from PyQt5.QtCore import QObject, pyqtSignal

import Server.Bot.jedol as jedol

class ServerSocket(QObject):
    update_signal = pyqtSignal(tuple, bool)
    recv_signal = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.bListen = False

        self.clients = []
        self.ip = []
        self.threads = []

        self.update_signal.connect(self.parent.updateClient) # setting
        self.recv_signal.connect(self.parent.updateMsg) # setting

    def __del__(self):
        self.stop()

    # Server
    def start(self, ip, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server.bind((ip, port))
        except Exception as e:
            print('Bind Error :', e)
            return False
        else:
            self.bListen = True

            self.t = Thread(target = self.listen, args = (self.server,))
            self.t.start()
            print('Server Listening...')

        return True

    def stop(self):
        self.bListen = False
        if hasattr(self, 'server'):
            self.server.close()
            print('Server STOP.')

    # Clients
    def listen(self, server):
        while self.bListen:
            server.listen(5)
            try:
                client, addr = server.accept()
            except Exception as e:
                print('Accept() Error :', e)
                break
            else:
                self.clients.append(client)
                self.ip.append(addr)
                
                self.update_signal.emit(addr, True)

                t = Thread(target = self.receive, args = (client, addr))
                self.threads.append(t)
                t.start()

    def receive(self, client, addr):
        while True:
            try:
                recv = client.recv(1024)
            except Exception as e:
                print('Recv() Error :', e)
                break
            else:
                msg = str(recv, encoding = 'utf-8')
                if msg:
                    self.send(msg)
                    self.recv_signal.emit(msg)
                    print('[RECV', addr, ']', msg)

                    # Command
                    jedol.Jedol(self, msg)

        self.removeClient(client, addr)

    def send(self, msg):
        try:
            for c in self.clients:
                c.send(msg.encode())
        except Exception as e:
            print('Send() Error :', e)

    def removeClient(self, client, addr):
        idx = -1
        for k, v in enumerate(self.clients):
            if v == client:
                idx = k
                break

        client.close()
        self.clients.remove(client)
        self.ip.remove(addr)
        del(self.threads[idx])

        self.update_signal.emit(addr, False)
        self.resource_Info()

    def removeAllClients(self):
        for c in self.clients:
            c.close()

        for addr in self.ip:
            self.update_signal.emit(addr, False)

        self.clients.clear()
        self.ip.clear()
        self.threads.clear()

    def resource_Info(self):
        print('Number of Client SOCKET\t:', len(self.clients))
        print('Number of Client IP\t:', len(self.ip))
        print('Number of Client THREAD\t:', len(self.threads))