import socket
from PyQt5.QtCore import QThread, pyqtSignal

class Client_Socket(QThread):
    recv_signal = pyqtSignal(str)
    def __init__(self, ip, port):
        super().__init__()

        self.ip = ip
        self.port = port

        self.sock = None
        self.running = True

    def run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((self.ip, self.port))
            while self.running:
                try:
                    msg = self.sock.recv(1024)
                    if not msg: break
                    self.recv_signal.emit(msg.decode())
                except OSError:
                    break
        except ConnectionRefusedError:
            self.recv_signal.emit('Connection refused.')
        finally:
            if self.sock:
                self.sock.close()

    def stop(self):
        self.running = False
        if self.sock:
            self.sock.close()
        self.quit()
        self.wait()