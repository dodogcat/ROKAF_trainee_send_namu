import json
import sqlalchemy
import pymysql


# with open("E:\\나무위키\\namuwiki_20210301.json", "r", encoding="UTF8") as st_json:
#     st_python = json.load(st_json)

# print(st_python)


def check_NS_End(str):
    if str.endswith(',"title":"') == True:
        return True
    else:
        return False

def check_TITLE_End(str):
    if str.endswith('","text":"') == True:
        return True
    else:
        return False

def check_TEXT_End(str):
    if str.endswith('","contributors":[') == True:
        return True
    else:
        return False

f = open("E:\\나무위키\\namuwiki_20210301.json", 'r', encoding="UTF-8")

# print(f.readline())
c = f.read(1)
mode = 'namespace'
namespace = ''
title = ''
text = ''

while c!='':
    c = f.read(13)

    if mode == 'namespace':
        while True:
            c = f.read(1)
            namespace += c
            if(check_NS_End(namespace) == True):
                namespace = namespace[0:-10]
                mode = 'title'
                break
    
    if mode == 'title':
        while True:
            c = f.read(1)
            title += c
            if(check_TITLE_End(title) == True):
                title = title[0:-10]
                mode = 'text'
                break
    
    if mode == 'text':
        while True:
            c = f.read(1)
            text += c
            if(check_TEXT_End(text) == True):
                text = text[0:-18]
                mode = 'namespace'
                break

    # delete contributes

    while c != ']':
        c = f.read(1)
    c = f.read(2)

    conn = pymysql.connect(host='127.0.0.1', user='root', password='!tnthd001', db='namu', charset='utf8mb4')

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
