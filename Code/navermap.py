from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
# 다운 받은 Chromedriver의 위치
path = 'D:/chromedriver/chromedriver.exe'
query = "왕십리 국밥집"
driver = webdriver.Chrome(path)

#네이버 지도 검색 url에 접근
driver.get('https://map.naver.com/v5/search')

#xpath로 네이버 지도 검색창 접근
elem = driver.find_element_by_xpath('/html/body/app/layout/div[2]/div[2]/div[1]/shrinkable-layout/search-layout/search-box/div/div[1]/div/input')

#검색창 element에 검색어 보내기
elem.send_keys(str(query))

#네이버 지도에 입력버튼이 없어서 엔터역할 
elem.send_keys(Keys.RETURN)

while True:
        
    #html 소스 가져오기
    html = driver.page_source

    #html을 python 객체로 변환하기
    soup = BeautifulSoup(html,'html.parser')

    # span tag 중에 class가 search_title_text인 것 찾기
    name = soup.find_all('span', class_='search_title_text')
    for i in name:
        print(i.string)

    # span tag 중에 class가 search_text category limit_100 ng-star-inserted인 것 찾기
    food = soup.find_all('span', class_='search_text category limit_100 ng-star-inserted')
    for i in food:
        print(i.string[1:])

    # span tag 중에 class가 search_text phone ng-star-inserted인 것 찾기    
    phone = soup.find_all('span', class_='search_text phone ng-star-inserted')
    for i in phone:
        print(i.string) 

    # span tag 중에 class가 search_text address인 것 찾기        
    addr = soup.find_all('span', class_='search_text address')
    for i in addr:
        print(i.string)

    elem = driver.find_element_by_xpath('/html/body/app/layout/div[2]/div[2]/div[1]/shrinkable-layout/search-layout/search-list/search-list-contents/div/div[2]/button[2]')
    if elem.is_enabled():
        elem.click()
        sleep(2)
    else:
        break
