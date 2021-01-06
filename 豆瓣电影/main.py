#coding=gbk
import requests
import time
import re
import json
from selenium import webdriver
from lxml import etree
opt = webdriver.ChromeOptions()
opt.set_headless() #设置driver配置为无头模式
driver=webdriver.Chrome('chromedriver.exe',options=opt)

def get_url(url):  #读取top250网站的html文本
    driver.get(url)
    html=driver.page_source #读取当前网页源码
    #print(html)
    return html

def get_main_num(html):
    hrefs=[] #用于存放top250主页网址的数组
    contain=etree.HTML(html)
    movies=contain.xpath('//*[@id="content"]/div/div[1]/ol/li') #读取网页一页数据有多少个电影
    i=1
    for movie in movies: #这里用个用不着的movie是为了代替1到25的循环，那样写不好看
        h=contain.xpath('//*[@id="content"]/div/div[1]/ol/li['+str(i)+']/div/div[2]/div[1]/a/@href')
        hrefs.append(h[0]) #将网址存入数组
        i+=1
    return hrefs

def get_main_infor(hrefs):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362'}
    for href in hrefs:
        try:
            driver.get(href)
            html=driver.page_source
            contain=etree.HTML(html)
            name=contain.xpath('//*[@id="content"]/h1/span[1]/text()')
            #writer=contain.xpath('//*[@id="info"]/span[1]/span[2]/text()')
            info=contain.xpath('//*[@id="link-report"]/span[1]/span/text()')
            write_txt(name[0].strip()+'\n')#strip()是用来删除空格的
            #print(info)
            try:
                write_txt(info[0].strip()+'\n')#因为主页不一样，简介的构成布局也不一样所以这里用个try区分，不然会出现以下读不到一下读的到的问题
                print('done')
            except:
                write_txt(contain.xpath('//*[@id="link-report"]/span[1]/text()')[0].strip() + '\n')#因为主页不一样，简介的构成布局也不一样所以这里用个try区分，不然会出现以下读不到一下读的到的问题
                print('done')
            time.sleep(11)
        except:
            html = requests.get(href, headers=headers)
            contain = etree.HTML(html.text)
            name = contain.xpath('//*[@id="content"]/h1/span[1]/text()')
            # writer=contain.xpath('//*[@id="info"]/span[1]/span[2]/text()')
            info = contain.xpath('//*[@id="link-report"]/span[1]/span/text()')
            write_txt(name[0].strip() + '\n')  # strip()是用来删除空格的
            # print(info)
            try:
                write_txt(info[0].strip() + '\n')  # 因为主页不一样，简介的构成布局也不一样所以这里用个try区分，不然会出现以下读不到一下读的到的问题
                print('done')
            except:
                write_txt(contain.xpath('//*[@id="link-report"]/span[1]/text()')[
                              0].strip() + '\n')  # 因为主页不一样，简介的构成布局也不一样所以这里用个try区分，不然会出现以下读不到一下读的到的问题
                print('done')
            time.sleep(11)

def write_txt(text):#写入txt
    with open('movies.txt','a',encoding='utf-8') as txt:
        txt.write(text)

def main():
    i=0
    while(i<250):
        url="https://movie.douban.com/top250?start="+str(i)
        html=get_url(url)
        hrefs=get_main_num(html)
        get_main_infor(hrefs)
        i+=25

if __name__ == '__main__':
    main()