import requests
from bs4 import BeautifulSoup
from urllib.parse import quote  # 올바른 임포트입니다

def lol():
    params = input("소환사 명: ")
    # '#'을 '-'로 바꾸기
    params = params.replace("#", "-")
    url = 'https://www.op.gg/summoners/kr/'
    target_url = url + quote(params)  # URL 인코딩
    html = requests.get(target_url).text

    soup = BeautifulSoup(html, 'html.parser')

    # 소환사명
    name = params

    try:
        # 언랭 판별
        is_unranked = soup.find("div", {"class": "TierRank unranked"}).get_text(strip=True)
        print(f"{name} 소환사님 정보입니다.")
        print("Tier: Unranked")
        print("본 정보는 op.gg의 검색결과를 바탕으로 제공됩니다!")
    except:
        try:
            # 솔로랭크 티어
            solo_tier = soup.find("div", {"class": "tier"}).get_text(strip=True)

            win_lose_div = soup.find("div", {"class": "win-lose"})
            wins = win_lose_div.contents[0].strip()  # 첫 번째 자식 노드의 텍스트 (승)
            losses = win_lose_div.contents[4].strip()  # 세 번째 자식 노드의 텍스트 (패)

            # 승률 정보
            win_ratio_div = soup.find("div", {"class": "ratio"})
            win_ratio = ''.join(win_ratio_div.stripped_strings)  # 모든 텍스트 노드 합침 (승률 포함)

            print(f"{name} 소환사님 정보입니다.")
            print("-----솔로랭크-----")
            print(f"티어: {solo_tier}")
            print(f"승&패: {wins} {losses}")
            print(f"승률: {win_ratio}")
        except Exception as e:
            print("솔로랭크 정보를 찾을 수 없습니다.")
            print(f"오류: {e}")

lol()



# def maple() :
# 	try :
# 		params = input("캐릭터 명 : ")
# 		url = 'https://maple.gg/u/'
# 		target_url = url + params
# 		html = requests.get(target_url).text

# 		soup = BeautifulSoup(html, 'html.parser')

# 		#레벨,직업,인기도
# 		user_mainInfo_box = soup.find_all("li", {"class":"user-summary-item"})
# 		#순위
# 		user_subInfo_box = soup.find_all("div", {"class":"col-lg-2 col-md-4 col-sm-4 col-6 mt-3"})
# 		#기타 기록 -> 필요 없을 듯해서 미구현
# 		#user_rankInfo_box = soup.find_all("div", {"class":"col-lg-3 col-6 mt-3 px-1"})

# 		name = params
# 		level = str(re.sub('<.+?>', '', str(user_mainInfo_box[0]), 0).strip())
# 		userClass = str(re.sub('<.+?>', '', str(user_mainInfo_box[1]), 0).strip())
# 		population = str(re.sub('<.+?>', '', str(user_mainInfo_box[2]), 0).strip()).replace("인기도","").strip()
# 		rank_all = str(re.sub('<.+?>', '', str(user_subInfo_box[0]), 0).strip()).replace("위","").strip()
# 		rank_world = str(re.sub('<.+?>', '', str(user_subInfo_box[1]), 0).strip()).replace("위","").strip().replace("\n","")
# 		rank_class_all = str(re.sub('<.+?>', '', str(user_subInfo_box[2]), 0).strip()).replace("위","").strip().replace("\n","")
# 		rank_class_world = str(re.sub('<.+?>', '', str(user_subInfo_box[3]), 0).strip()).replace("위","").strip().replace("\n","")
# 		guild = str(soup.find_all("div", {"class": "col-lg-2 col-md-4 col-sm-4 col-12 mt-3"})[0]).split(">")[4].split("<")[0]

# 		#미구현 항목(무릉, 시드, 유니온{유니온이 고렙 아니면 .gg에서 적용 안됨})
# 		#rank_murung = user_rankInfo_box.find_all("div", {"class" : "text-secondary"})
# 		#rank_seed = user_rankInfo_box.find_all("div", {"class" : "mb-3"})
# 		#union = user_rankInfo_box.find_all("div", {"class" : "mb-3"})
# 		#union_level = user_rankInfo_box.find_all("div", {"class" : "mb-3"})

# 		print("닉네임 :", name)
# 		print("레벨 :", level)
# 		print("직업 :", userClass)
# 		print("인기도 :", population)
# 		print("길드 :", guild)
# 		#print("유니온 :", union, union_level)
# 		#print("무릉 최고기록 :", rank_murung)
# 		#print("더 시드 최고기록 :", rank_seed)
# 		print(rank_all+"위")
# 		print(rank_world+"위")
# 		print(rank_class_world+"위")
# 		print(rank_class_all+"위")
# 		print("본 정보는 메이플.gg의 검색 결과를 바탕으로 제공됩니다.")
# 	except :
# 		print("캐릭터를 찾을 수 없어요...")