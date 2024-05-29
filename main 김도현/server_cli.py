import socketserver
from jedol_bot.jedol import Jedol

port = 8274

class MyHandler(socketserver.BaseRequestHandler):
    users = {}
    def handle(self):
        while True:
            self.request.send('채팅 닉네임을 전송하세요.'.encode())
            nickname = self.request.recv(1024).decode()

            if nickname in self.users:
                self.request.send('이미 등록된 닉네임입니다.\n'.encode())
            else:
                self.users[nickname] = (self.request, self.client_address)

                for sock, _ in self.users.values():
                    sock.send(f'{nickname}님이 입장했습니다.'.encode())

                print(f'현재 {len(self.users)}명 참여 중...')
                break

        while True:
            msg = self.request.recv(1024)
                        
            if msg.decode() == '/exit':
                print('exit client')
                self.request.close()
                break

            for sock, _ in self.users.values():
                sock.send(f'[{nickname}] {msg.decode()}'.encode())
                Jedol(sock, msg.decode())

        if nickname in self.users:
            del self.users[nickname]

            for sock, _ in self.users.values():
                sock.send(f'{nickname}님이 퇴장했습니다.'.encode())

            print(f'현재 {len(self.users)}명 참여 중...')
            
class Chat_SERVER(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

server = Chat_SERVER(('', port), MyHandler)
server.serve_forever()

server.shutdown()
server.server_close()