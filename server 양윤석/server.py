import socketserver

class MyHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print(self.client_address)

class ChatServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

server = ChatServer(("", 8274), MyHandler)