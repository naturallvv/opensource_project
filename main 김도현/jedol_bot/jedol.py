import random

class Jedol:
    def __init__(self, sock, command):
        self.sock = sock

        if command == '/제돌이':
            randnum = random.randint(1, 4)
            self.sock.send('-------제돌이 v0.1-------\n'.encode())
            self.sock.send('기능 소개는 기능, ㄱㄴ을 입력하세요.\n\n'.encode())

            if randnum == 1:
                self.sock.send('[제돌이] 무엇을 도와드릴까요?\n'.encode())
            elif randnum == 2:
                self.sock.send('[제돌이] 무엇이든 물어보세요!\n'.encode())
            elif randnum == 3:
                self.sock.send('[제돌이] 어떤 것을 도와드려요?\n'.encode())
            else:
                self.sock.send('[제돌이] 무엇이든 말씀하세요!\n'.encode())

        elif command == '/제바':
            self.sock.send('[제돌이] 이용해줘서 감사해요!\n'.encode())

        elif command == '/기능' or command ==  '/ㄱㄴ':
            self.funcText()

        elif command == '/학식':
            pass
            
        elif command == '/셔틀':
            # station.main()
            pass

        elif command == '/날씨':
            # weather.weather()
            pass

        elif command == '/공지':
            # notice.get_jnu_notice()
            pass

        elif command == '/게임':
            # game.lol()
            pass

        elif command.startswith('/'):
            randnum = random.randint(1, 4)
            if randnum == 1:
                self.sock.send('[제돌이] 무슨 말인지 모르겠어요. 좀 더 쉬운 언어로 말씀해주시겠어요?\n'.encode())
            elif randnum == 2:
                self.sock.send('[제돌이] 무슨 뜻이에요? 혹시 좀 더 쉬운 단어가 있나요?\n'.encode())
            elif randnum == 3:
                self.sock.send('[제돌이] 잘 모르겠어요. 저는 어려운 말은 잘 몰라요.\n'.encode())
            else:
                self.sock.send('[제돌이] 제가 잘 모르는 말이에요. 그건 조금 더 공부해올게요.\n'.encode())

    def funcText(self):
        self.sock.send('-----------기능-----------\n'.encode())
        self.sock.send('학식 식단표 : 학식\n'.encode())
        self.sock.send('셔틀 시간표 : 셔틀\n'.encode())
        self.sock.send('날씨 : 날씨\n'.encode())
        self.sock.send('학사 공지 : 공지\n'.encode())
        self.sock.send('게임전적검색 : 게임\n'.encode())
        self.sock.send('제돌이 끄기 : 제바\n'.encode())