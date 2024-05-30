import requests
from bs4 import BeautifulSoup

import random

# import game
# import station
# import weather
# import notice

class Jedol:
    def __init__(self, parent, msg):
        self.parent = parent

        parts = msg.split(' ')
        if len(parts) > 1 and parts[1].startswith('/'):
            command = parts[1]
            if command == '/제돌이':
                self.parent.send("-------제돌이 v0.1-------\n기능 소개는 기능, ㄱㄴ을 입력하세요.\n")

                randnum = random.randint(1, 4)
                if randnum == 1:
                    self.parent.send("무엇을 도와드릴까요?")
                elif randnum == 2:
                    self.parent.send("무엇이든 물어보세요!")
                elif randnum == 3:
                    self.parent.send("어떤 것을 도와드려요?")
                else:
                    self.parent.send("무엇이든 말씀하세요!")
            
            elif command == '/제바':
                self.parent.send("이용해줘서 감사해요!")

            elif command == '/기능':
                self.parent.send("-----------기능-----------\n셔틀 시간표 : 셔틀\n날씨 : 날씨\n학사 공지 : 공지\n게임전적검색 : 게임")
            
            elif command == '/셔틀':
                #station.main()
                pass

            elif command == '/날씨':
                #weather.weather()
                pass

            elif command == '/공지':
                self.get_jnu_notice()
                pass

            elif command == '/게임':
                #game.lol()
                pass

            else:
                randnum = random.randint(1, 4)
                if randnum == 1:
                    self.parent.send("무슨 말인지 모르겠어요. 좀 더 쉬운 언어로 말씀해주시겠어요?")
                elif randnum == 2:
                    self.parent.send("무슨 뜻이에요? 혹시 좀 더 쉬운 단어가 있나요?")
                elif randnum == 3:
                    self.parent.send("잘 모르겠어요. 저는 어려운 말은 잘 몰라요.")
                else:
                    self.parent.send("제가 잘 모르는 말이에요. 그건 조금 더 공부해올게요.")

    def get_jnu_notice(self):
        url = "https://jejunu.ac.kr/index.htm"
        
        # 페이지 요청
        response = requests.get(url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        # 학사 공지 추출
        try:
            notices = soup.find('div', class_='new_notice').find_all('li')
            titles = []
            dates = []
            links = []
            
            for notice in notices:
                title = notice.find('span', class_='title').get_text(strip=True)
                date = notice.find('span', class_='date').get_text(strip=True)
                href = notice.find('a')['href']
                full_url = "https://jejunu.ac.kr" + href
                titles.append(title)
                dates.append(date)
                links.append(full_url)
            
            # 결과 출력
            self.parent.send("JNU 알림 1페이지 자료입니다.\n")
            for i in range(len(titles)):
                self.parent.send(f"날짜: {dates[i]}\n")
                self.parent.send(f"제목: {titles[i]}\n")
                self.parent.send(f"링크: {links[i]}\n")
                self.parent.send("---------------\n")
            self.parent.send("자세한 사항은 URL을 눌러 확인하세요.\n")
            self.parent.send("본 정보는 제주대학교 홈페이지를 바탕으로 제공됩니다.\n")
        
        except AttributeError as e:
            self.parent.send("학사 공지를 찾을 수 없습니다.\n")
            self.parent.send(e)