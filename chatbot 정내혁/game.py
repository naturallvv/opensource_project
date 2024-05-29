import requests
from bs4 import BeautifulSoup
from urllib.parse import quote  # 올바른 임포트입니다

def lol():
    params = input("소환사 명(ex 소환사#KR1): ")
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