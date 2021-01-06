import requests
import sys
import time
import csv
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from pprint import pprint
from lxml import etree
chrome_options = Options()
chrome_options.add_argument("--headless")
driver=webdriver.Chrome(chrome_options=chrome_options)

def get_all_information():
    titles=[]
    url='http://data.stats.gov.cn/easyquery.htm?cn=A01'
    driver.get(url)
    time.sleep(5)
    #close=driver.find_element_by_css_selector('body > div.tc.experience > em')
    #close.click()
    i=2
    temp = '102.2'
    while(i<635):
        target = driver.find_element_by_css_selector('#treeZhiBiao_'+str(i)+'_ico')
        driver.execute_script("arguments[0].scrollIntoView();", target)
        time.sleep(1)
        elem=driver.find_element_by_css_selector('#treeZhiBiao_'+str(i)+'_ico')
        elem.click()
        html = driver.page_source
        result=etree.HTML(html)
        t=result.xpath('//*[@id="table_main"]/tbody/tr[1]/td[2]/text()')
        name=result.xpath('//*[@id="treeZhiBiao_'+str(i)+'_span"]/text()')
        if(t==temp):
            pass
        else:
            j=1
            html=driver.page_source
            r=etree.HTML(html)
            rr=r.xpath('//*[@id="main-container"]/div[2]/div[2]/div[2]/div/div[3]/table/tbody/tr/td[1]/text()')
            while(j<len(rr)):
                k=2
                title=r.xpath('//*[@id="main-container"]/div[2]/div[2]/div[2]/div/div[3]/table/tbody/tr['+str(j)+']/td[1]/text()')
                #print(title)
                while(k<14):
                    times=r.xpath('//*[@id="main-container"]/div[2]/div[2]/div[2]/div/div[2]/table/thead/tr/th['+str(k)+']/strong/text()')
                    num=r.xpath('//*[@id="table_main"]/tbody/tr['+str(j)+']/td['+str(k)+']/text()')
                    #print(times)
                    #print(num)
                    put_data_in_CSV(title,times,num,name)
                    k+=1
                j+=1
            temp=t
        i+=1

def put_data_in_CSV(name, time, data, s):
    i = 0
    t = 0
    all = []
    all.append(name)
    all.append(time)
    all.append(data)
    # print(all)
    out = open(s[0]+'.csv', 'a', newline='')
    csv_write = csv.writer(out, dialect='excel')
    csv_write.writerow(all)

get_url()