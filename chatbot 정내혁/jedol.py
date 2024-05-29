import game
import station
import wheather
import notice
import menu
import random

#기능 보여줄 함수
def funcText():
    print("-----------기능-----------")
    print("학식 식단표 : 학식, ㅎㅅ")
    print("셔틀 시간표 : 셔틀, ㅅㅌ")
    print("날씨 : 날씨, ㄴㅆ")
    print("학사 공지 : 공지, ㄱㅈ")
    print("게임전적검색 : 게임, ㄱㅇ")
    print("제돌이 끄기 : 제바, ㅈㅂ")

# 산돌이 메인 함수
def start() :
    print("-------제돌이 v0.1-------")
    print("기능 소개는 기능, ㄱㄴ을 입력하세요.")
    inp = '' # 발화 정보를 담는 변수
    inp2 = '' # 세부 발화 정보를 담는 변수
    randnum = 0 # 다양한 대답을 선택 할 난수를 담을 변수
    while 1 :
        #랜덤 변수를 통해서 대답 선택
        randnum = random.randint(1,4)

        if randnum == 1 :
            print("무엇을 도와드릴까요?")
        elif randnum == 2 :
            print("무엇이든 물어보세요!")
        elif randnum == 3 :
            print("어떤 것을 도와드려요?")
        else :
            print("무엇이든 말씀하세요!")

        inp = input()
        if '기능' in inp or 'ㄱㄴ' in inp:
            funcText()
        elif '학식' in inp or 'ㅎㅅ' in inp or '메뉴' in inp or 'ㅁㄴ' in inp or '밥' in inp or 'ㅂ' in inp or '배고' in inp:
            menu.menu()
        elif '셔틀' in inp or 'ㅅㅌ' in inp:
            station.main()
        elif '날씨' in inp or 'ㄴㅆ' in inp :
            wheather.weather()
        elif '공지' in inp or 'ㄱㅈ' in inp :
            notice.get_jnu_notice()
        elif '게임' in inp or 'ㄱㅇ' in inp:
            while 1 :
                game.lol()
        elif '산바' in inp or 'ㅅㅂ' in inp :
            print("이용해줘서 감사해요!")
            break
        else :
            if randnum == 1 :
                print("무슨 말인지 모르겠어요. 좀 더 쉬운 언어로 말씀해주시겠어요?")
            elif randnum == 2 :
                print("무슨 뜻이에요? 혹시 좀 더 쉬운 단어가 있나요?")
            elif randnum == 3 :
                print("잘 모르겠어요. 저는 어려운 말은 잘 몰라요.")
            else :
                print("제가 잘 모르는 말이에요. 그건 조금 더 공부해올게요.")