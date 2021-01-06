#coding=gbk
import requests
import time
import re
import json
from selenium import webdriver
from lxml import etree
opt = webdriver.ChromeOptions()
opt.set_headless() #����driver����Ϊ��ͷģʽ
driver=webdriver.Chrome('chromedriver.exe',options=opt)

def get_url(url):  #��ȡtop250��վ��html�ı�
    driver.get(url)
    html=driver.page_source #��ȡ��ǰ��ҳԴ��
    #print(html)
    return html

def get_main_num(html):
    hrefs=[] #���ڴ��top250��ҳ��ַ������
    contain=etree.HTML(html)
    movies=contain.xpath('//*[@id="content"]/div/div[1]/ol/li') #��ȡ��ҳһҳ�����ж��ٸ���Ӱ
    i=1
    for movie in movies: #�����ø��ò��ŵ�movie��Ϊ�˴���1��25��ѭ��������д���ÿ�
        h=contain.xpath('//*[@id="content"]/div/div[1]/ol/li['+str(i)+']/div/div[2]/div[1]/a/@href')
        hrefs.append(h[0]) #����ַ��������
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
            write_txt(name[0].strip()+'\n')#strip()������ɾ���ո��
            #print(info)
            try:
                write_txt(info[0].strip()+'\n')#��Ϊ��ҳ��һ�������Ĺ��ɲ���Ҳ��һ�����������ø�try���֣���Ȼ��������¶�����һ�¶��ĵ�������
                print('done')
            except:
                write_txt(contain.xpath('//*[@id="link-report"]/span[1]/text()')[0].strip() + '\n')#��Ϊ��ҳ��һ�������Ĺ��ɲ���Ҳ��һ�����������ø�try���֣���Ȼ��������¶�����һ�¶��ĵ�������
                print('done')
            time.sleep(11)
        except:
            html = requests.get(href, headers=headers)
            contain = etree.HTML(html.text)
            name = contain.xpath('//*[@id="content"]/h1/span[1]/text()')
            # writer=contain.xpath('//*[@id="info"]/span[1]/span[2]/text()')
            info = contain.xpath('//*[@id="link-report"]/span[1]/span/text()')
            write_txt(name[0].strip() + '\n')  # strip()������ɾ���ո��
            # print(info)
            try:
                write_txt(info[0].strip() + '\n')  # ��Ϊ��ҳ��һ�������Ĺ��ɲ���Ҳ��һ�����������ø�try���֣���Ȼ��������¶�����һ�¶��ĵ�������
                print('done')
            except:
                write_txt(contain.xpath('//*[@id="link-report"]/span[1]/text()')[
                              0].strip() + '\n')  # ��Ϊ��ҳ��һ�������Ĺ��ɲ���Ҳ��һ�����������ø�try���֣���Ȼ��������¶�����һ�¶��ĵ�������
                print('done')
            time.sleep(11)

def write_txt(text):#д��txt
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