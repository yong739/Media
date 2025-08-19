import re
import base64
import requests
import hashlib
import configparser

headers = {'User-Agent': 'okhttp/3.15'}

def get_fan_conf():
    config = configparser.ConfigParser()
    config.read("config.ini")
    url = 'http://www.饭太硬.net/tv/'
    response = requests.get(url, headers=headers)
    match = re.search(r'[A-Za-z0]{8}\*\*(.*)', response.text)
    if not match:
        return
    result = match.group(1)
    m = hashlib.md5()
    m.update(result.encode('utf-8'))
    md5 = m.hexdigest()
    try:
        old_md5 = config.get("md5", "conf")
        if md5 == old_md5:
            print("No update needed")
            return
    except:
        pass
    content = base64.b64decode(result).decode('utf-8')
    url_match = re.search(r'spider"\:"(.*);md5;', content)
    if url_match:
        url = url_match.group(1)
        content = content.replace(url, './jar/fan.txt')
    content = diy_conf(content)
    with open('old.json', 'w', newline='', encoding='utf-8') as f:
        f.write(content)
    local_content = local_conf(content)
    with open('fan.json', 'w', newline='', encoding='utf-8') as f:
        f.write(local_content)
    config.set("md5", "conf", md5)
    with open("config.ini", "w") as f:
        config.write(f)
    jmd5_match = re.search(r';md5;(\w+)"', content)
    if jmd5_match:
        jmd5 = jmd5_match.group(1)
        current_md5 = config.get("md5", "jar").strip()
        if jmd5 != current_md5:
            config.set("md5", "jar", jmd5)
            with open("config.ini", "w") as f:
                config.write(f)
            response = requests.get(url)
            with open("./jar/fan.txt", "wb") as f:
                f.write(response.content)

def diy_conf(content):
    content = content.replace('备用公众号【叨观荐影】', '豆瓣')
    pattern = r'{"key":"Bili".*?\n{"key":"Biliych".*?\n'
    content = re.sub(pattern, '', content, flags=re.S)
    return content

def local_conf(content):
    # 在"米搜"条目前插入采集站，保留其他内容不变
    pattern = r'(?=({"key":"抠搜"))'
    insertion = (
        '{"key":"百度","name":"百度┃采集","type":1,"api":"https://api.apibdzy.com/api.php/provide/vod?ac=list","searchable":1,"filterable":0},\n'
        '{"key":"量子","name":"量子┃采集","type":0,"api":"https://cj.lziapi.com/api.php/provide/vod/at/xml/","searchable":1,"changeable":1},\n'
        '{"key":"非凡","name":"非凡┃采集","type":0,"api":"http://cj.ffzyapi.com/api.php/provide/vod/at/xml/","searchable":1,"changeable":1},\n'
        '{"key":"暴風","name":"暴風┃采集","type":1,"api":"https://bfzyapi.com/api.php/provide/vod/?ac=list","searchable":1,"changeable":1},\n'
        '{"key":"索尼","name":"索尼┃采集","type":1,"api":"https://suoniapi.com/api.php/provide/vod","searchable":1,"changeable":1},\n'
        '{"key":"快帆","name":"快帆┃采集","type":1,"api":"https://api.kuaifan.tv/api.php/provide/vod","searchable":1,"changeable":1},\n'
    )
    content = re.sub(pattern, insertion, content, flags=re.S)
    return content

if __name__ == '__main__':
    get_fan_conf()
