import threading
import requests
from bs4 import BeautifulSoup
import json
import os
import re

def get_html(url): #获得网页源代码
    s=requests.Session()
    s.keep_alive = False
    requests.adapters.DEFAULT_RETRIES = 5
    page=s.get(url)
    # page=requests.get(url,headers={'Connection':'close'})
    # print(page.text)
    return page.text

def get_img(page): #寻找网页中的图片并下载
    soup=BeautifulSoup(page,"html.parser")
    imgs=soup.findAll("img") #获取源代码中的img图片
    srcs=[]
    names=[]
    for img in imgs:
        try:
            src=img.get("src") #从img中获取src中的字段
            # print(src)
            src2 = src[src.rfind("/"):]#获取最后一个/后的字段
            name=src2.split('/')#删除/
            # print(name)
            t=threading.Thread(target=download_img,args=(src,name[0]))#新的进程去下载图片
            t.start()
        except:
            continue

def get_hrefs(page):#获取其他页面
    soup=BeautifulSoup(page,"html.parser")
    nets=soup.findAll("a")#寻找所有a的信息
    hrefs=[]
    for net in nets:
        href=net.get("href")#获取所有href后的网页
        hrefs.append(href)
    # print(hrefs)
    return hrefs

def get_again(hrefs,depth):#深度指定用户的深度，该深度必须大于或等于1
    while(depth>1):
        for href in hrefs:#通过每个链接循环
            try:
                page=get_html(href)
                get_img(page)
                hrefs_A=get_hrefs(page)
            except:
                continue
        get_again(hrefs_A,depth-1)#递归处理下一个深度

def put_depth(url,depth):#递归句柄next depthDepth指定用户的深度，该深度必须大于或等于1
    page=get_html(url)
    hrefs=get_hrefs(page)
    # print(hrefs)
    get_again(hrefs,depth)

def download_img(src,name):#下载图片
    s = requests.Session()
    print(src)
    if 'feieee' in src:
        src = src.replace('blog.feieee.com', '47.99.187.54')
        src2 = src[src.rfind("/"):]  # Get the last / following text
        if '-' in src2:
            result = src2.split('-')
            result2 = src2.split('.')
        end = result[0] + '.' + result2[1]
        src = src.replace(src2, end)
    if 'feimax' in src:
        src = src.replace('blog.feimax.com', '47.99.187.54')
    r = s.get(src)
    name=src.split('http://')
    src2 = src[src.rfind("/"):]
    path_name=name[1].split(src2)
    isExists = os.path.exists("./imgs/"+path_name[0])
    if not isExists:
        path="./imgs/"+path_name[0]
        path=path.replace('/','\\')
        os.makedirs(path)
        f = open("./imgs/" + name[1], 'wb')
        f.write(r.content)
        f.close()
        print("已经下载完成")
        return True
    else:
        f = open("./imgs/" + name[1], 'wb')
        f.write(r.content)
        f.close()
        print("已经下载完成")
        return False

def main():
    url="http://www.feimax.com"
    page=get_html(url)
    get_img(page)
    put_depth(url,2)

if __name__ == '__main__':
    main()