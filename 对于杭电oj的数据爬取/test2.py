import requests
import os
import csv
import json
import xlrd
import time
import re
import datetime
import sys
import pymongo
import pandas as pd
from bs4 import BeautifulSoup
from lxml import etree
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
driver=webdriver.Chrome()

result=[]
driver.get('http://acm.hdu.edu.cn/status.php?first=&pid=1002&user=xgk1705xct&lang=0&status=0')
html=driver.page_source
b=BeautifulSoup(html,'lxml').find('table',align="center").find('div',id="fixed_table").find_all('tr')
for i in b:
    bb=i.find_all('td')
    result.append(bb[2].get_text())
print(result)