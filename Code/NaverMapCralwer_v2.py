from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import json

# 다운 받은 Chromedriver의 위치
path = 'D:/chromedriver/chromedriver.exe'
query = "왕십리 국밥집"
driver = webdriver.Chrome(path)

#음식점 정보 담기위한 dictionary타입 변수 선언
store = dict()

#음식점 이름을 key로 사용하기엔 중복이 존재할 가능성이 있어서 숫자를 key로 사용
num = 1

#네이버 지도 검색 url에 접근
driver.get('https://map.naver.com/v5/search')
#페이지 로딩 시간이 필요 
sleep(3)

#xpath로 네이버 지도 검색창 접근
elem = driver.find_element_by_xpath('/html/body/app/layout/div[2]/div[2]/div[1]/shrinkable-layout/search-layout/search-box/div/div[1]/div/input')

#검색창 element에 검색어 보내기
elem.send_keys(str(query))

#네이버 지도에 입력버튼이 없어서 엔터역할 
elem.send_keys(Keys.RETURN)

# 마지막 페이지까지 반복하기 위한 것
while True:
        
    #html 소스 가져오기
    html = driver.page_source

    #html을 python 객체로 변환하기
    soup = BeautifulSoup(html,'html.parser')

    # span tag 중에 class가 search_title_text인 것 찾기
    name = soup.find_all('span', class_='search_title_text')
    # span tag 중에 class가 search_text category limit_100 ng-star-inserted인 것 찾기
    food = soup.find_all('span', class_='search_text category limit_100 ng-star-inserted')
    # span tag 중에 class가 search_text phone ng-star-inserted인 것 찾기    
    phone = soup.find_all('span', class_='search_text phone ng-star-inserted')
    # span tag 중에 class가 search_text address인 것 찾기        
    addr = soup.find_all('span', class_='search_text address')

    for na, fd, ph, ad in zip(name, food, phone, addr):
        store[num] = {'name': na.string,'food' : fd.string[1:],'phone' : ph.string, 'address': ad.string}
        num+=1
        
    #xpath로 다음 버튼 element 접근
    elem = driver.find_element_by_xpath('/html/body/app/layout/div[2]/div[2]/div[1]/shrinkable-layout/search-layout/search-list/search-list-contents/div/div[2]/button[2]')
    
    #button이 활성화되어 있는지 비활성화 되어 있는지 확인
    if elem.is_enabled(): 
        #button 클릭 후 다음 페이지가 로딩되어야 함으로 sleep함수 사용
        elem.click() 
        sleep(2)
    else:
        break

#with open을 사용시 나중에 close를 해줄 필요가 없음
with open('foodstore.json','w',encoding='utf-8') as writefile:
    #ensure_ascii = 한글이 유니코드로 보이는 것을 막기위한 것, 
    json.dump(store,writefile,ensure_ascii=False,indent='\t')
