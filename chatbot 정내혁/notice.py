import requests
from bs4 import BeautifulSoup

def get_jnu_notice():
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
        print("JNU 알림 1페이지 자료입니다.")
        for i in range(len(titles)):
            print(f"날짜: {dates[i]}")
            print(f"제목: {titles[i]}")
            print(f"링크: {links[i]}")
            print("---------------")
        print("자세한 사항은 URL을 눌러 확인하세요.")
        print("본 정보는 제주대학교 홈페이지를 바탕으로 제공됩니다.")
    
    except AttributeError as e:
        print("학사 공지를 찾을 수 없습니다.")
        print(e)