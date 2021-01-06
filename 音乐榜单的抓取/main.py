import requests
import os
import json
from collections import Counter #计数的库


def __init__(self, log_file_name="my.log"):
    # 默认的域名
    self.host = "http://www.kuwo.cn"
    # 根据关键字key获取歌曲的rid值的json数据的接口
    self.rid_url = "/api/www/search/searchMusicBykeyWord?key={}"
    # 根据rid获取歌曲下载链接的json数据的接口
    self.mp3_url = "/url?rid={}&type=convert_url3&br=128kmp3"
    # 获取音乐榜 可以得到sourceid
    self.bang_menu = "/api/www/bang/bang/bangMenu"
    # 获取音乐信息的接口
    self.music_info = "/api/www/music/musicInfo?mid={}"
    # 根据 musicid 获取歌词信息
    self.song_lyric = "http://m.kuwo.cn/newh5/singles/songinfoandlrc?musicId={}"
    # 根据bangid 获取音乐列表
    self.music_list = "/api/www/bang/bang/musicList?bangId={}&pn={}&rn={}"
    # 一些必要的请求头
    self.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
        "Referer": "http://www.kuwo.cn/search/list",  # 这个请求头没有的话，会出现 403 Forbidden
        "csrf": "0HQ0UGKNAKR",  # CSRF Token Not Found!
        # CSRF Token Not Found!
        "Cookie": "Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1584003311; _ga=GA1.2.208068437.1584003311; _gid=GA1.2.1613688009.1584003311; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1584017980; kw_token=0HQ0UGKNAKR; _gat=1",
    }

def __del__(self):
    self.f.close()

def get_rank(id,url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
        "Referer": "http://www.kuwo.cn/search/list",  # 这个请求头没有的话，会出现 403 Forbidden
        "csrf": "0HQ0UGKNAKR",  # CSRF Token Not Found!
        # CSRF Token Not Found!
        "Cookie": "Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1584003311; _ga=GA1.2.208068437.1584003311; _gid=GA1.2.1613688009.1584003311; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1584017980; kw_token=0HQ0UGKNAKR; _gat=1",
    }
    # url1=get_nextrank(url)
    r=requests.get(url,headers=headers)#带头访问排行榜接口，不带头会出现被反爬
    ht=r.text
    music_id = []
    music_name = []    #此三个列表用于保存歌曲数据
    music_author = []
    html = json.loads(ht)
    h1 = html['data']['musicList']
    for i in h1:
        music_id.append(i['rid'])
        music_name.append(i['name'].split('(')[0])
        music_author.append(i['artist'])
    print(music_id, music_name, music_author)
    for i in range(len(music_id)):
        download(id, music_id[i], music_name[i], music_author[i])
    most = check(music_author)
    notice(most)

def download(id,rid,name,author):
    try:
        m=requests.get("http://www.kuwo.cn/url?rid="+str(rid)+"&type=convert_url3&br=128kmp3") #读取歌曲数据
        filepath = os.path.join(id, name+' '+author + '.mp3')
        if not os.path.exists(id):
            os.mkdir(id)
        with open(filepath, mode='wb') as file:
            file.write(m.content)
        print('歌曲下载成功')
    except:
        pass

def check(name):
    collection_words = Counter(name)
    most_counterNum = collection_words.most_common(3) #进行列表中歌手的出现次数排序
    print(most_counterNum)
    return most_counterNum

def notice(most_counterNum):
    first=most_counterNum[0]
    second=most_counterNum[1]
    third=most_counterNum[2]
    first=list(first)
    second=list(second)
    third=list(third)
    print("榜单中出现次数最多的是:"+first[0]+"出现次数为"+str(first[1])+','
          +second[0]+"出现次数为"+str(second[1])+','
          +third[0]+"出现次数为"+str(third[1]))

def main():
    list=['酷我飙升榜','酷我新歌榜','酷我热歌榜','抖音热歌榜']
    dict = {'酷我飙升榜': 'http://www.kuwo.cn/api/www/bang/bang/musicList?bangId=93&pn=1&rn=100&httpsStatus=1&reqId=588ce030-b6fd-11ea-8283-bf20c8b775b9',
            '酷我新歌榜': 'http://www.kuwo.cn/api/www/bang/bang/musicList?bangId=17&pn=1&rn=100&httpsStatus=1&reqId=5012cbb0-b705-11ea-8283-bf20c8b775b9',
            '酷我热歌榜': 'http://www.kuwo.cn/api/www/bang/bang/musicList?bangId=16&pn=1&rn=100&httpsStatus=1&reqId=63442030-b705-11ea-8283-bf20c8b775b9',
            '抖音热歌榜': 'http://www.kuwo.cn/api/www/bang/bang/musicList?bangId=158&pn=1&rn=100&httpsStatus=1&reqId=6c9efe20-b705-11ea-8283-bf20c8b775b9',}
    for i in range(len(list)):
        print(dict[list[i]])
        get_rank(list[i],dict[list[i]])


if __name__ == '__main__':
    main()