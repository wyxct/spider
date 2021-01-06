import os
import json
import time
import requests
import pymongo
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pprint import pprint
from lxml import etree

def get_url(url):
    html=requests.get(url)
    html1=json.loads(html.content.decode())
    result=html1['returndata']
    i=0
    j=0
    if type(result)==type("str"):
        print(html1)
        result1=eval(result)
    else:
        result1=result
        print(2)
    for i in range(len(result1['wdnodes'][0]['nodes'])):
        try:
            mainname=result1['datanodes'][i]['code']
            name = result1['wdnodes'][0]['nodes'][i]['cname']
            for j in range(13):
                time=result1['wdnodes'][1]['nodes'][j]['cname']
                data=result1['datanodes'][j]['data']['strdata']
                print(name)
                print(time)
                print(data)
                get_data_in(name,time,data)
        except:
            break

def get_data_in(name,time,data):
    myclient=pymongo.MongoClient('mongodb://localhost:27017/')
    mydb=myclient['国家数据']
    mycol=mydb['价格指数']
    mydict={"指数名":name,"时间":time,"指数":data}
    mycol.insert_one(mydict)

def remain():
    i=1
    while(i<20):
        try:
            if i<10:
                num='0'+str(i)
            else:
                num=str(i)
            url='http://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=hgyd&rowcode=zb&colcode=sj&wds=%5B%5D&dfwds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A0101'+num+'%22%7D%5D'
            get_url(url)
            i+=1
        except:
            break

def main():
    flag=0
    now=datetime.datetime.now()
    times=datetime.datetime(now.year,now.month,now.day,now.hour,now.minute,now.second)+datetime.timedelta(seconds=3)
    while(True):
        now=datetime.datetime.now()
        if(times<now):
            time.sleep(86400)
            remain()
            flag=1
        else:
            if flag==1:
                times=times+datetime.timedelta(seconds=5)
                flag=0

if __name__=='__main__':
    main()