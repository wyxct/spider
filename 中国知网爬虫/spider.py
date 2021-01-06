import os
import requests
import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
driver=webdriver.Chrome()

def get_url():
    url='http://epub.cnki.net/kns/subPage/Total.aspx'
    html=driver.get(url)
    html=driver.page_source
    a_all=BeautifulSoup(html,'lxml').find_all('div',class_='item')
    for a in a_all:
        b_all=a.find_all('dl')
        for b in b_all:
            c_all=b.find_all('dd')
            for c in c_all:
                t=c.get_text()
                fp=open('中国知网资源总库.txt','a',encoding='utf-8')
                fp.write(t+'\n')
                s=c.find('a',class_='hastip')
                if s is None:
                    sh='NULL'
                    fp.write('简介：')
                    fp.write(sh + '\n')
                else:
                    sh=s.get('show')
                    if sh is None:
                        sh='NULL'
                    fp.write('简介：')
                    fp.write(sh+'\n')

def main():
    get_url()

if __name__=='__main__':
    main()




