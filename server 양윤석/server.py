import socketserver

class MyHandler(socketserver.BaseRequestHandler):
    users = {}

    def handle(self):
        
        while True:
            self.request.send('Please Send Your NAME'.encode())
            nickname = self.request.recv(1024).decode()
            if nickname in self.users:
                self.request.send('This NAME is Already Registered.\n'.encode())
            else:
                self.users[nickname] = (self.request, self.client_address)

            for sock, _ in self.users.values():
                sock.send(f'{nickname}님이 입장했습니다.'.encode())
                
            print(f'Concurrent Users : {len(self.users)}')
            break

        
        while True:
            msg = self.request.recv(1024)
            if msg.decode() == '/exit':
                self.request.close()
                break

            for sock, _ in self.users.values():
                sock.send(f'[{nickname}] {msg.decode()}'.encode())

        
        if nickname in self.users:
            del self.users[nickname]

            for sock, _ in self.users.values():
                sock.send(f'{nickname}님이 퇴장했습니다.'.encode())
                
            print(f'Concurrent Users : {len(self.users)}') 

class Chat_SERVER(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

server = Chat_SERVER(('', 8274), MyHandler)
server.serve_forever()

server.shutdown()
server.server_close()