# import requests
# from bs4 import BeautifulSoup

# # 웹사이트 URL
# url = 'https://cms.jejunu.ac.kr/camp/stud/foodmenu.htm'

# # GET 요청을 보내 웹페이지 가져오기
# response = requests.get(url)

# # 요청이 성공했는지 확인
# if response.status_code == 200:
#     # BeautifulSoup을 사용하여 HTML 파싱
#     soup = BeautifulSoup(response.content, 'html.parser')
    
#     # 메뉴 정보를 포함한 테이블 찾기
#     table = soup.find('table', {'class': 'contents-table'})

#     # 메뉴 정보를 저장할 리스트 초기화
#     menu_info = []

#     # 테이블의 각 행(iterate) 반복
#     for row in table.find_all('tr'):
#         # 날짜 셀 찾기
#         date_cell = row.find('th', {'rowspan': '1'})
#         if date_cell:
#             date = date_cell.text.strip()
        
#         # 메뉴 셀 찾기
#         menu_cell = row.find('td')
#         if menu_cell:
#             menu = menu_cell.get_text(separator=', ').strip()
#             menu_info.append(f"{date} 점심 메뉴: {menu}")

#     # 추출한 메뉴 정보 출력
#     for info in menu_info:
#         print(info)
# else:
#     print(f"웹페이지를 가져오는데 실패했습니다. 상태 코드: {response.status_code}")
