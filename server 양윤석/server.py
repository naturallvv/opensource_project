import socketserver

class MyHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print(self.client_address)
        while True:
            msg = self.request.recv(1024)
            if msg.decode() == "/bye":
                print("exit client")
                self.request.close()
                break
            self.request.send(msg)

class ChatServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

server = ChatServer(("", 8275), MyHandler)
server.serve_forever()
server.shutdown()
server.server_close()