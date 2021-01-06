import requests
import sys
import json
import time
import datetime
import pymongo
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pprint import pprint
from lxml import etree
from selenium.webdriver.common.keys import Keys

def dosth():
    print(1)

def main():
    flag=0
    now=datetime.datetime.now()
    times=datetime.datetime(now.year,now.month,now.day,now.hour,now.minute,now.second)+datetime.timedelta(seconds=3)
    while(True):
        now=datetime.datetime.now()
        if(times<now):
            time.sleep(86400)
            dosth()
            flag=1
        else:
            if flag==1:
                times=times+datetime.timedelta(seconds=5)
                flag=0

if __name__=='__main__':
    main()