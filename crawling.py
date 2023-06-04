import time

import requests
from bs4 import BeautifulSoup
import pprint
import json
import re


# URL 설정
url = "https://www.inha.ac.kr/kr/1072/subview.do"

# 페이지 요청
response = requests.get(url)

# 페이지 내용을 BeautifulSoup으로 파싱
soup = BeautifulSoup(response.content, 'html.parser')

# objHeading_h2 클래스를 가진 요소 추출하여 titles에 저장
titles = [title.text for title in soup.find_all(class_="objHeading_h2")]

# foodInfoWrap 클래스를 가진 요소 추출하여 menus에 저장
menus = [menu for menu in soup.find_all(class_="foodInfoWrap")]

# title 값을 "xx-xx" 형식으로 바꾸어 dates에 저장
dates = [re.sub(r'\((\d{2})\.(\d{2})\.\)', r'\1-\2', title) for title in titles]

# 결과를 저장할 data 딕셔너리 초기화
data = {}

# 메뉴 정보 추출
for date, menu in zip(dates, menus):

    print("날짜:", date)
    time.sleep(0.5)
    menu_data = {}  # 메뉴 정보를 담을 딕셔너리

    # 운영 시간 추출
    operation_time = menu.find(class_="hSp15 objHeading_h3").text
    start_time, end_time = operation_time.split(" ~ ")

    # 구분, 상세메뉴, 가격 추출
    rows = menu.find('tbody').find_all('tr')
    menu_items = []

    for row in rows:
        columns = row.find_all('td')

        구분 = columns[0].text.strip()
        상세메뉴 = columns[1].text.split("<br>")
        가격 = columns[2].text.strip().replace('원', '').replace(',', '')

        상세메뉴 = [item.strip() for item in 상세메뉴]

        상세메뉴 = 상세메뉴[0].split('\r')

        menu_item = {
            "구분": 구분,
            "가격": 가격,
            "상세메뉴": 상세메뉴
        }

        print(menu_item)
        time.sleep(0.5)
        menu_items.append(menu_item)

    if "/" in start_time:
        스낵바, 바, 셀프라면, start_time = start_time.split(" ")
        식 = 스낵바 + 바 + 셀프라면
    else:
        식, start_time = start_time.split(" ")


    print("메뉴분류:", 식)
    time.sleep(0.5)

    start_time = start_time.replace("(", "")
    end_time = end_time.replace(")", "")

    menu_data[식] = {}

    menu_data[식]["메뉴"] = menu_items
    menu_data[식]["운영시간"] = [start_time, end_time]

    # 요일별로 데이터 정리
    day_of_week = date.split()[0].replace("-", "")
    meal_type = date.split()[1]

    if meal_type not in data:
        data[meal_type] = {}
        data[meal_type] = menu_data
    else:
        data[meal_type][식] = menu_data[식]


# 출력
print('데이터 출력')
time.sleep(0.5)
pprint.pprint(data)


print('json에 저장')
time.sleep(0.5)

json_data = json.dumps(data, indent=4, ensure_ascii=False)

# JSON 파일에 데이터 저장
with open("data.json", "w", encoding="utf-8") as file:
    file.write(json_data)