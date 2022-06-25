import json
import sqlalchemy
import pymysql

# namespace의 끝을 확인합니다. 다음 데이터인 title의 앞부분인 잡다한 정보까지 받습니다.
def check_NS_End(str):
    if str.endswith(',"title":"') == True:
        return True
    else:
        return False
    
# tit;e의 끝을 확인합니다. 다음 데이터인 text의 앞부분인 잡다한 정보까지 받습니다.
def check_TITLE_End(str):
    if str.endswith('","text":"') == True:
        return True
    else:
        return False

# text의 끝을 확인합니다. 다음 데이터인 contribute의 앞부분인 잡다한 정보까지 받습니다.
def check_TEXT_End(str):
    if str.endswith('","contributors":[') == True:
        return True
    else:
        return False

# 파일이 용량이 크기 때문에 조금씩 읽어야 한다.
f = open("E:\\나무위키\\namuwiki_20210301.json", 'r', encoding="UTF-8")

c = f.read(1)
mode = 'namespace'
namespace = ''
title = ''
text = ''

while c!='':
    # 한 루프마다 하나의 JSON 객체의 정보 추출
    # namespace 까지의 잡다한 정보 제거
    c = f.read(13)

    if mode == 'namespace':
        while True:
            c = f.read(1)
            namespace += c
            if(check_NS_End(namespace) == True):
                # 잡다한 정보 제거
                namespace = namespace[0:-10]
                mode = 'title'
                break
    
    if mode == 'title':
        while True:
            c = f.read(1)
            title += c
            if(check_TITLE_End(title) == True):
                # 잡다한 정보 제거
                title = title[0:-10]
                mode = 'text'
                break
    
    if mode == 'text':
        while True:
            c = f.read(1)
            text += c
            if(check_TEXT_End(text) == True):
                # 잡다한 정보 제거
                text = text[0:-18]
                mode = 'namespace'
                break

    # delete contributes
    while c != ']':
        c = f.read(1)
    c = f.read(2)
    
    # 대충 sql에 저장하기
    conn = pymysql.connect(host='127.0.0.1', user='root', password='암호', db='namu', charset='utf8mb4')

    cur = conn.cursor()

    title = title.replace("'", " ")
    text = text.replace("'", " ")


    sql = f"replace into wiki values({namespace}, '{title}', '{text}')"
    print(sql)
    cur.execute(sql)

    conn.commit()

    namespace = ''
    title= ''
    text= ''

conn.close()
