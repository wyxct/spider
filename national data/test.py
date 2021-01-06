import requests
import sys
import time
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pprint import pprint
from lxml import etree
driver=webdriver.Chrome()

def get_url():
    titles=[]
    url='http://data.stats.gov.cn/easyquery.htm?cn=A01'
    driver.get(url)
    i=2
    while(i<15):
        target = driver.find_element_by_id('treeZhiBiao_'+str(i)+'_span')
        driver.execute_script("arguments[0].scrollIntoView();", target)
        time.sleep(0.5)
        elem=driver.find_element_by_css_selector('#treeZhiBiao_'+str(i)+'_span')
        elem.click()
        i+=1
    j=15
    while(j<635):
        target = driver.find_element_by_css_selector('#treeZhiBiao_'+str(j)+'_ico')
        driver.execute_script("arguments[0].scrollIntoView();", target)
        time.sleep(1)
        elem=driver.find_element_by_css_selector('#treeZhiBiao_'+str(j)+'_ico')
        elem.click()
        html = driver.page_source
        try:
            t=BeautifulSoup(html,'lxml').find('ul',id='treeZhiBiao_'+str(j)+'_ul')
            j+=1
        except:
            result=etree.HTML(html)
            t=result.xpath('//*[@id="main-container"]/div[2]/div[2]/div[2]/div/div[3]/table/tbody/tr[1]/td[1]/text()')
            num=result.xpath('//*[@id="table_main"]/tbody/tr[1]/td/text()')
            print(t)
            print(num)
            j+=1

get_url()
