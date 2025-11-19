import re
import base64
import requests
import hashlib
import configparser

headers = {'User-Agent': 'okhttp/3.15'}

def get_fan_conf():
    config = configparser.ConfigParser()
    config.read("config.ini")
    url = 'http://www.饭太硬.com/tv/'
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
    with open('fan.json', 'w', newline='', encoding='utf-8') as f:
        f.write(content)
    local_content = local_conf(content)
    with open('new.json', 'w', newline='', encoding='utf-8') as f:
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
    # 在"抠搜"条目前插入采集站，保留其他内容不变
    pattern = r'(?=({"key":"抠搜"))'
    insertion = (
        '{"key": "👖木耳","name":"✈️木耳┃采集", "type":1,"api": "https://heimuer.ggff.net/api.php/tvbox","searchable":1,"changeable":1},\n'
        '{"key": "👖魔爪","name":"✈️魔爪┃采集","type":1,"api": "https://mozhuazy.com/api.php/provide/vod/?ac=list","searchable":1,"changeable":1},\n'
        '{"key": "👖电影天堂","name":"电影天堂┃采集","type":1,"api": "http://caiji.dyttzyapi.com/api.php/provide/vod/?ac=list","searchable":1,"changeable":1},\n'
        '{"key": "👖豆瓣","name":"✈️豆瓣┃采集","type":1,"api": "https://caiji.dbzy5.com/api.php/provide/vod/from/dbm3u8/at/josn","searchable":1,"changeable":1},\n'
        '{"key": "👖茅台","name":"✈️茅台┃采集","type":1,"api": "https://caiji.maotaizy.cc/api.php/provide/vod/from/mtm3u8/at/josn","searchable":1,"changeable":1},\n'
        '{"key": "👖如意","name":"✈️如意┃采集","type":1,"api": "http://cj.rycjapi.com/api.php/provide/vod/?ac=list","searchable":1,"changeable":1},\n'
        '{"key": "👖量子","name":"✈️量子┃采集","type":1,"api": "https://cj.lziapi.com/api.php/provide/vod/?ac=list","searchable":1,"changeable":1},\n'
        '{"key": "👖卧龙","name":"✈️卧龙┃采集","type":1,"api": "https://collect.wolongzy.cc/api.php/provide/vod/at/xml/?ac=list","searchable":1,"changeable":1},\n'
        '{"key": "👖暴风","name":"✈️暴风┃采集","type":1,"api": "http://by.bfzyapi.com/api.php/provide/vod","searchable":1,"changeable":1},\n'
        '{"key": "👖360","name":"✈️360┃采集","type":1,"api": "https://360zyzz.com/api.php/provide/vod/from/360m3u8/at/json","searchable":1,"changeable":1},\n'
        '{"key": "👖极速","name":"✈️极速┃采集","type":1,"api": "https://jszyapi.com/api.php/provide/vod/from/jsm3u8/at/json","searchable":1,"changeable":1},\n'
        '{"key": "👖U酷","name":"✈️U酷┃采集","type":1,"api": "https://api.ukuapi88.com/api.php/provide/vod/?ac=list","searchable":1,"changeable":1},\n'
        '{"key": "👖天涯","name":"✈️天涯┃采集","type":1,"api": "https://tyyszyapi.com/api.php/provide/vod/?ac=list","searchable":1,"changeable":1},\n'
        '{"key": "👖无尽","name":"✈️无尽┃采集","type":1,"api": "https://api.wujinapi.me/api.php/provide/vod/?ac=list","searchable":1,"changeable":1},\n'
        '{"key": "👖iQIYI","name":"✈️iQIYI┃采集","type":1,"api": "https://iqiyizyapi.com/api.php/provide/vod/from/snm3u8/at/xml","searchable":1,"changeable":1},\n'
        '{"key": "👖ikun","name":"✈️ikun┃采集","type":1,"api": "https://ikunzyapi.com/api.php/provide/vod/from/ikm3u8/at/json","searchable":1,"changeable":1},\n'
        '{"key": "👖魔都","name":"✈️魔都┃采集","type":1,"api": "https://www.mdzyapi.com/api.php/provide/vod/?ac=list","searchable":1,"changeable":1},\n'
        '{"key": "👖百度云","name":"✈️百度云┃采集","type":1,"api": "https://api.apibdzy.com/api.php/provide/vod/?ac=list","searchable":1,"changeable":1},\n'
        '{"key": "👖闪电","name":"✈️闪电┃采集","type":1,"api": "https://xsd.sdzyapi.com/api.php/provide/vod/?ac=list","searchable":1,"changeable":1},\n'
        '{"key": "👖红牛","name":"✈️红牛┃采集","type":1,"api": "https://www.hongniuzy2.com/api.php/provide/vod/from/hnm3u8/at/josn","searchable":1,"changeable":1},\n'
        '{"key": "👖光速","name":"✈️光速┃采集","type":1,"api": "https://api.guangsuapi.com/api.php/provide/vod/from/gsm3u8","searchable":1,"changeable":1},\n'
        '{"key": "👖新浪","name":"✈️新浪┃采集","type":1,"api": "https://api.xinlangapi.com/xinlangapi.php/provide/vod/from/xlm3u8","searchable":1,"changeable":1},\n'
        '{"key": "👖快车","name":"✈️快车┃采集","type":1,"api": "https://caiji.kuaichezy.org/api.php/provide/vod/?ac=list","searchable":1,"changeable":1},\n'
        '{"key": "👖金鹰","name":"✈️金鹰┃采集","type":1,"api": "https://jyzyapi.com/provide/vod/from/jinyingm3u8/at/json","searchable":1,"changeable":1},\n'
        '{"key": "👖猫眼","name":"✈️猫眼┃采集","type":1,"api": "https://api.maoyanapi.top/api.php/provide/vod","searchable":1,"changeable":1},\n'
        '{"key": "👖旺旺","name":"✈️旺旺┃采集","type":1,"api": "https://api.wwzy.tv/api.php/provide/vod/?ac=list","searchable":1,"changeable":1},\n'
        '{"key": "👖虎牙","name":"✈️虎牙┃采集","type":1,"api": "https://www.huyaapi.com/api.php/provide/vod/from/hym3u8/at/json","searchable":1,"changeable":1},\n'
        '{"key": "👖豪华","name":"✈️豪华┃采集","type":1,"api": "https://hhzyapi.com/api.php/provide/vod/from/hhm3u8/at/json","searchable":1,"changeable":1},\n'
        '{"key": "👖速播","name":"✈️速播┃采集","type":1,"api": "https://subocj.com/api.php/provide/vod/from/subm3u8/at/json","searchable":1,"changeable":1},\n'
        '{"key": "👖非凡","name":"✈️非凡┃采集","type":1,"api": "http://api.ffzyapi.com/api.php/provide/vod/?ac=list","searchable":1,"changeable":1},\n'
        '{"key": "👖樱花","name":"✈️樱花┃采集","type":1,"api": "https://m3u8.apiyhzy.com/api.php/provide/vod/?ac=list","searchable":1,"changeable":1},\n'
        '{"key": "👖优质","name":"✈️优质┃采集","type":1,"api": "http://api.yzzy-api.com/inc/apijson.php?ac=list","searchable":1,"changeable":1},\n'
        '{"key": "👖鸭鸭","name":"✈️鸭鸭┃采集","type":1,"api": "https://cj.yayazy.net/api.php/provide/vod/?ac=list","searchable":1,"changeable":1},\n'
        '{"key": "👖瀑布","name":"✈️瀑布┃采集","type":1,"api": "https://dh.ha.cn/api.php/provide/vod/?ac=list","searchable":1,"changeable":1},\n'
        '{"key": "👖牛牛","name":"✈️牛牛┃采集","type":1,"api": "https://api.niuniuzy.me/api.php/provide/vod/from/nnm3u8/at/xml","searchable":1,"changeable":1},\n'
        '{"key": "👖最大","name":"✈️最大┃采集","type":1,"api": "http://zuidazy.me/api.php/provide/vod","searchable":1,"changeable":1},\n'
        '{"key": "👖飘零","name":"✈️飘零┃采集","type":1,"api": "https://p2100.net/api.php/provide/vod","searchable":1,"changeable":1},\n'
        '{"key": "👖1080","name":"✈️1080┃采集","type":1,"api": "https://api.1080zyku.com/inc/apijson.php","searchable":1,"changeable":1},\n'
        '{"key": "👖神马","name":"✈️神马┃采集","type":1,"api": "https://img.smdyw.top/api.php/provide/vod","searchable":1,"changeable":1},\n'
    )
    content = re.sub(pattern, insertion, content, flags=re.S)
    return content

if __name__ == '__main__':
    get_fan_conf()
