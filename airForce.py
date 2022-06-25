from turtle import goto
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pymysql

name = '혹시 꽉차면 admin을'
password = 'admin'
title = '아니 애러 왜 건너 뜀?'
content = '하지만 귀찮으니 패스'
friend = '입력해 삭제하시면 됩니다'

def sending(soldier):
        # Initialize Web Driver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-dev-shm-usage")
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager(log_level=0).install()), options=options)
    # driver = webdriver.Chrome(ChromeDriverManager().install())
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    # 기본군사훈련단
    url = 'https://www.airforce.mil.kr/user/indexSub.action?codyMenuSeq=156893223&siteId=last2&menuUIType=sub'

    driver.get(url)
    driver.maximize_window()
    action = ActionChains(driver)
    driver.implicitly_wait(10)  


    # 훈련병 정보에 맞게 값을 바꾸세요
    if soldier=='훈련병이름1':
        # Input Soldier Information
        driver.find_element_by_css_selector('#searchName').send_keys('훈련병이름1') 
        driver.find_element_by_css_selector('#birthYear').send_keys('생년')
        driver.find_element_by_css_selector('#birthMonth').send_keys('생월')
        driver.find_element_by_css_selector('#birthDay').send_keys('생일')
        driver.find_element_by_css_selector('#btnNext').click()

    else:
        driver.find_element_by_css_selector('#searchName').send_keys('훈련병이름2') 
        driver.find_element_by_css_selector('#birthYear').send_keys('생년')
        driver.find_element_by_css_selector('#birthMonth').send_keys('생월')
        driver.find_element_by_css_selector('#birthDay').send_keys('생일')
        driver.find_element_by_css_selector('#btnNext').click()

    # Click Search Soldier Button
    driver.switch_to.window(driver.window_handles[1])
    driver.find_element_by_css_selector('.choice').click()

    # Click Write Letter Button
    driver.switch_to.window(driver.window_handles[0])
    driver.find_element_by_css_selector('#btnNext').click()

    # Click Input Address Button
    driver.find_element_by_xpath("//div[@class='UIbtn']/span[@class='wizBtn large Ngray normal btnR']").click()
    driver.find_element_by_css_selector('#senderZipcode').click()

    # Default Address is Soldier Himself
    driver.switch_to.window(driver.window_handles[1])
    driver.find_element_by_css_selector('.popSearchInput').send_keys("자기 집주소")
    driver.find_element_by_xpath("/html/body/form[2]/div/div/div[1]/div[1]/fieldset/span/input[2]").click()
    driver.find_element_by_xpath("/html/body/form[2]/div/div/div[1]/div[2]/table/tbody/tr[1]/td[2]/a/div/div").click()
    driver.find_element_by_css_selector('#rtAddrDetail').send_keys("세부주소")
    driver.find_element_by_css_selector('.btn-bl').click()

    # Input Letter Contents
    driver.switch_to.window(driver.window_handles[0])
    driver.find_element_by_css_selector('#senderName').send_keys(name)
    driver.find_element_by_css_selector('#relationship').send_keys(friend)
    driver.find_element_by_css_selector('#title').send_keys(title)
    driver.find_element_by_css_selector('#contents').send_keys(content)
    driver.find_element_by_css_selector('#password').send_keys(password)
    driver.find_element_by_css_selector('.submit').click()

    cur_url = driver.current_url

    driver.quit()

    if (cur_url.find('saveEmailSuccess') != -1):
        print("die")
        return False
    else:
        return True

def randomFromNamu():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='암호', db='namu', charset='utf8mb4')

    cur = conn.cursor()

    sql = """
        select a.*
        from (
            select title
            from wiki
            order by RAND()
            LIMIT 1
        ) b join wiki a on b.title = a.title
        """
    # print(sql)
    cur.execute(sql)

    row = cur.fetchone()

    # print(row)

    return row[1], row[2]

    
send_wiki = True

if send_wiki== True:
    for i in range(0,180):
        
        if i % 2 == 0:
            title, content = randomFromNamu()
            if content[0:9] == '#redirect':
                i = i - 1
                continue


            if len(content) > 1150:
                content = content[0:1150]
            content = content.replace('include','')
            content = content.replace('style','')

            try:
                out = sending('최다운')
                if out:
                    print(content)
            except:
                i = i - 1
                continue


        else:
            title, content = randomFromNamu()
            if content[0:9] == '#redirect':
                i = i - 1
                continue

            if len(content) > 1150:
                content = content[0:1150]
                
            content = content.replace('include','')
            content = content.replace('style','')

            try:
                out = sending('전인우')
                if out:
                    print(content)
            except:
                i = i - 1
                continue


    exit()

# 이 부분은 난중일기를 보내는 부분
f = open("G:\내 드라이브\군머\난중일기.txt", 'r', encoding="UTF-8")
index_text = open("G:\내 드라이브\군머\index.txt", 'r')
index = int(index_text.read())

full = f.read()
full = full.split('\n')

# 30줄 씩 보낼 예정
for i in range(0,90):

    title = "bible : " + str(int(index/30))
    content = ''
    for j in range(0,30):
        content = content + "\n" +full[index + j]
    sending('훈련병이름1')
    index = index + 30


    title = "bible : " + str(int(index/30))
    content = ''
    for j in range(0,30):
        content = content + "\n" +full[index + j]
    sending('훈련병이름2')
    index = index + 30

# 마지막까지 보낸 인덱스 저장
end = open("G:\내 드라이브\군머\index.txt", 'w')
end.write(str(index))
end.close()
index_text.close()
f.close()
