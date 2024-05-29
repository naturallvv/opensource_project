import requests
from datetime import datetime
from bs4 import BeautifulSoup

def weather():
    try:
        url = 'https://search.naver.com/search.naver?query='
        aria = input("어떤 지역 날씨를 보여드릴까요?").strip()
        aria = aria.replace("날씨", "")
        url += (aria + " 날씨")

        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')

        # 지역 정보
        aria_det = soup.find("h2", {"class": "title"})
        aria_det_text = aria_det.get_text(strip=True)
        aria_det = aria_det_text

        #기온 정보
        temp_container = soup.find("div", {"class": "temperature_text"})
        if temp_container:
            today_temp_strong = temp_container.find("strong")
            if today_temp_strong:
                today_temp_text = today_temp_strong.get_text(strip=True)
                today_temp = today_temp_text
            else:
                raise ValueError("기온 정보를 찾을 수 없습니다.")
        else:
            raise ValueError("기온 컨테이너를 찾을 수 없습니다.")
        
        # 코멘트 박스
        today_com = soup.find("p", {"class": "summary"})
        if today_com:
            today_com_text = today_com.get_text(strip=True)
            today_com = today_com_text
        else:
            raise ValueError("코멘트 정보를 찾을 수 없습니다.")

        # 자외선 정보
        uv_container = soup.find("li", {"class": "item_today level1"})
        if uv_container:
            today_ray_strong = uv_container.find("strong", {"class": "title"})
            today_ray_span = uv_container.find("span", {"class": "txt"})
            if today_ray_strong and today_ray_span:
                today_ray_text = today_ray_span.get_text(strip=True)
                today_ray = today_ray_text
            else:
                raise ValueError("자외선 정보를 찾을 수 없습니다.")
        else:
            raise ValueError("자외선 컨테이너를 찾을 수 없습니다.")

        # 미세먼지 정보
        dust_container = soup.find("li", {"class": "item_today level2"})
        if dust_container:
            today_dust_strong = dust_container.find("strong", {"class": "title"})
            today_dust_span = dust_container.find("span", {"class": "txt"})
            if today_dust_strong and today_dust_span:
                today_dust_text = today_dust_span.get_text(strip=True)
                today_dust = today_dust_text
            else:
                raise ValueError("미세먼지 정보를 찾을 수 없습니다.")
        else:
            raise ValueError("미세먼지 컨테이너를 찾을 수 없습니다.")
        
        # 초미세먼지 정보
        ultrafine_dust_container = soup.find_all("li", {"class": "item_today level2"})[1]
        if ultrafine_dust_container:
            today_ultrafine_dust_strong = ultrafine_dust_container.find("strong", {"class": "title"})
            today_ultrafine_dust_span = ultrafine_dust_container.find("span", {"class": "txt"})
            if today_ultrafine_dust_strong and today_ultrafine_dust_span:
                today_ultrafine_dust_text = today_ultrafine_dust_span.get_text(strip=True)
                today_ultrafine_dust = today_ultrafine_dust_text
            else:
                raise ValueError("초미세먼지 정보를 찾을 수 없습니다.")
        else:
            raise ValueError("초미세먼지 컨테이너를 찾을 수 없습니다.")
        
        # 오존 정보
        ozone_container = soup.find_all("li", {"class": "item_today level1"})[1]
        if ozone_container:
            today_ozone_strong = ozone_container.find("strong", {"class": "title"})
            today_ozone_span = ozone_container.find("span", {"class": "txt"})
            if today_ozone_strong and today_ozone_span:
                today_ozone_text = today_ozone_span.get_text(strip=True)
                today_ozone = today_ozone_text
            else:
                raise ValueError("오존 정보를 찾을 수 없습니다.")
        else:
            raise ValueError("오존 컨테이너를 찾을 수 없습니다.")

        print(datetime.today().strftime("%Y%m%d"))
        print(f"{aria_det}의 날씨입니다.")
        print(f"금일 평균기온: {today_temp}˚C")
        print(f"오늘은 {today_com.replace('˚', '˚C')}")
        print(f"자외선: {today_ray}")
        print(f"미세먼지: {today_dust}")
        print(f"초미세먼지: {today_ultrafine_dust}")
        print(f"오존: {today_ozone}")
        print("본 정보는 네이버 검색 결과를 바탕으로 제공됩니다.")

    except Exception as e:
        print("지역을 찾을 수 없거나 동일한 지역명이 여러 개 존재해요!")
        print("ex)연동 -> 제주시연동")
        print(f"Error: {e}")

weather()
