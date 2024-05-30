import socket
from threading import Thread
from PyQt5.QtCore import QObject, pyqtSignal

class Signal(QObject):
    recv_signal = pyqtSignal(str)
    disconnect_signal = pyqtSignal()

class ClientSocket:
    def __init__(self, parent):
        self.parent = parent

        self.bConnect = False

        self.recv = Signal()
        self.recv.recv_signal.connect(self.parent.updateMsg) # setting

        self.disconnect = Signal()
        self.disconnect.disconnect_signal.connect(self.parent.updateDisconnect) # setting

    def __del__(self):
        self.stop()

    # Client
    def start(self, ip, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect((ip, port))
        except Exception as e:
            print('Connect Error :', e)
            return False
        else:
            self.bConnect = True
            
            self.t = Thread(target = self.receive, args = (self.client,))
            self.t.start()
            print('Connected')

        return True
    
    def stop(self):
        self.bConnect = False
        if hasattr(self, 'client'):
            self.client.close()
            print('Client STOP.')

            del(self.client)
            self.disconnect.disconnect_signal.emit()

    def receive(self, client):
        while self.bConnect:
            try:
                recv = client.recv(1024)
            except Exception as e:
                print('Recv() Error :', e)
                break
            else:
                msg = str(recv, encoding = 'utf-8')
                if msg:
                    self.recv.recv_signal.emit(msg)
                    print('[RECV]', msg)

        self.stop()

    def send(self, name, msg):
        if not self.bConnect:
            return
        try:
            send_msg = f'[{name}] {msg}'
            self.client.send(send_msg.encode())
        except Exception as e:
            print('Send() Error :', e)