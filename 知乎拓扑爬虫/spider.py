import os
import time
import requests
import sys
import re
# from pyquery import PyQuery as pq
from bs4 import BeautifulSoup
import json
from pprint import pprint
headers = {'Accept': '*/*',
               'Accept-Language': 'en-US,en;q=0.8',
               'Cache-Control': 'max-age=0',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
               'Connection': 'keep-alive',
               'Referer': 'http://www.baidu.com/'
               }

def get_url(url):
    html=requests.get(url,headers=headers)
    return html

def get_dict(html):
    html1=html.content.decode()
    result=json.loads(html1)['data']
    #pprint(result)
    return result

def get_num(result):
    number=len(result)
    #print(number)
    return number

def get_information(result,number):
    i=0
    for i in range(number):
        name=result[i]['name']
        id=result[i]['url_token']
        print(name+':'+id)

def get_newurl(result,number):
    i=0
    if get_num(result)==0:
        print('end')
        exit(0)
    id=result[i]['url_token']
    newurl="https://www.zhihu.com/api/v4/members/"+id+"/followees?include=data%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=20"
    return newurl

def main():
    i=0
    url='https://www.zhihu.com/api/v4/members/madisonand34/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=20'
    html=get_url(url)
    result=get_dict(html)
    number=get_num(result)
    get_information(result,number)
    new=get_newurl(result,number)
    for i in range(10):
        html = get_url(new)
        result = get_dict(html)
        number = get_num(result)
        get_information(result, number)
        new = get_newurl(result,number)

if __name__ == '__main__':
    main()


