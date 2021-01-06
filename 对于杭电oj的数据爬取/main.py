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
from bs4 import BeautifulSoup
from lxml import etree
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
driver=webdriver.Chrome()

def get_data_in_CSV(username, rank, accepted):     #将数据放入CSV格式文件中
    i = 0
    t = 0
    all = []
    all.append(username)
    all.append(rank)
    all.append(accepted)
    # print(all)
    out = open('oj' + '.csv', 'a', newline='')
    csv_write = csv.writer(out, dialect='excel')
    csv_write.writerow(all)
    print('生成csv文件成功!')

def get_data_in_CSV_by_year(username, num):     #将数据放入CSV格式文件中
    i = 0
    t = 0
    all = []
    all.append(username)
    all.append(num)
    # print(all)
    out = open('oj_by_year' + '.csv', 'a', newline='')
    csv_write = csv.writer(out, dialect='excel')
    csv_write.writerow(all)
    print('生成csv文件成功!')

def get_data_in_CSV_by_month(username, num):     #将数据放入CSV格式文件中
    i = 0
    t = 0
    all = []
    all.append(username)
    all.append(num)
    # print(all)
    out = open('oj_by_month' + '.csv', 'a', newline='')
    csv_write = csv.writer(out, dialect='excel')
    csv_write.writerow(all)
    print('生成csv文件成功!')

def get_data_in_CSV_by_day(username, num):     #将数据放入CSV格式文件中
    i = 0
    t = 0
    all = []
    all.append(username)
    all.append(num)
    # print(all)
    out = open('oj_by_day' + '.csv', 'a', newline='')
    csv_write = csv.writer(out, dialect='excel')
    csv_write.writerow(all)
    print('生成csv文件成功!')

def get_data_in_db(username, rank, accepted):      #将数据放入数据库中
    myclient=pymongo.MongoClient('mongodb://localhost:27017/')
    mydb=myclient['oj']
    mycol=mydb['oj情况']
    mydict={'用户名':username,'排名':rank,'刷题数':accepted}
    mycol.insert_one(mydict)

def get_information(username):      #得到杭电的刷题基础信息
    url = 'http://acm.hdu.edu.cn/userstatus.php?user=' + username
    driver.get(url)
    html=driver.page_source
    #print(html)
    result=etree.HTML(html)
    username=result.xpath('/html/body/table/tbody/tr[4]/td/table/tbody/tr/td/h1/text()')
    rank=result.xpath('/html/body/table/tbody/tr[4]/td/table/tbody/tr/td/table/tbody/tr[2]/td[2]/text()')
    accepted=result.xpath('/html/body/table/tbody/tr[4]/td/table/tbody/tr/td/table/tbody/tr[4]/td[2]/text()')
    result1={'用户名':username[0],'杭电排名':rank[0],'完成题目量':accepted[0]}
    print(result1)

def get_condition(username):      #得到杭电刷题的每题提交量和通过次数
    i=0
    t=[]
    url = 'http://acm.hdu.edu.cn/userstatus.php?user=' + username
    driver.get(url)
    html = driver.page_source
    result=etree.HTML(html)
    questions=result.xpath('/html/body/table/tbody/tr[4]/td/table/tbody/tr/td/p[3]/a/text()')
    answers=result.xpath('/html/body/table/tbody/tr[4]/td/table/tbody/tr/td/p[3]/font/text()')
    while(i<len(questions)):
        tt=questions[i]+':'+answers[i]
        t.append(tt)
        i+=1
    print(t)

def get_all_information():      #根据文件目录下的CSV文件，读取其中的姓名和用户名来生成一个刷题报表
    i=0
    workbook = xlrd.open_workbook(r'name.xlsx')
    sheet1_name = workbook.sheet_names()[0]
    sheet1 = workbook.sheet_by_index(0)
    cols=sheet1.col_values(0)
    while(i<len(cols)):
        username = sheet1.row_values(i)[1]
        url = 'http://acm.hdu.edu.cn/userstatus.php?user=' + username
        driver.get(url)
        html = driver.page_source
        # print(html)
        result = etree.HTML(html)
        username = result.xpath('/html/body/table/tbody/tr[4]/td/table/tbody/tr/td/h1/text()')
        rank = result.xpath('/html/body/table/tbody/tr[4]/td/table/tbody/tr/td/table/tbody/tr[2]/td[2]/text()')
        accepted = result.xpath('/html/body/table/tbody/tr[4]/td/table/tbody/tr/td/table/tbody/tr[4]/td[2]/text()')
        result1 = {'用户名': username[0], '杭电排名': rank[0], '完成题目量': accepted[0]}
        print(result1)
        i+=1

def get_all_information_in_csv():      #根据文件目录下的CSV文件，读取其中的姓名和用户名来生成一个刷题报表，存入CSV中
    i=0
    workbook = xlrd.open_workbook(r'name.xlsx')
    sheet1_name = workbook.sheet_names()[0]
    sheet1 = workbook.sheet_by_index(0)
    cols=sheet1.col_values(0)
    while(i<len(cols)):
        username = sheet1.row_values(i)[1]
        url = 'http://acm.hdu.edu.cn/userstatus.php?user=' + username
        driver.get(url)
        html = driver.page_source
        # print(html)
        result = etree.HTML(html)
        username = result.xpath('/html/body/table/tbody/tr[4]/td/table/tbody/tr/td/h1/text()')
        rank = result.xpath('/html/body/table/tbody/tr[4]/td/table/tbody/tr/td/table/tbody/tr[2]/td[2]/text()')
        accepted = result.xpath('/html/body/table/tbody/tr[4]/td/table/tbody/tr/td/table/tbody/tr[4]/td[2]/text()')
        get_data_in_CSV(username,rank,accepted)
        i+=1

def get_all_information_in_db():       #根据文件目录下的CSV文件，读取其中的姓名和用户名来生成一个刷题报表，存入数据库中
    i=0
    workbook=xlrd.open_workbook(r'name.xlsx')
    sheet1_name=workbook.sheet_names()[0]
    sheet1=workbook.sheet_by_index(0)
    cols=sheet1.col_values(0)
    while(i<len(cols)):
        username=sheet1.row_values(i)[1]
        url='http://acm.hdu.edu.cn/userstatus.php?user=' + username
        driver.get(url)
        html=driver.page_source
        result=etree.HTML(html)
        username = result.xpath('/html/body/table/tbody/tr[4]/td/table/tbody/tr/td/h1/text()')
        rank = result.xpath('/html/body/table/tbody/tr[4]/td/table/tbody/tr/td/table/tbody/tr[2]/td[2]/text()')
        accepted = result.xpath('/html/body/table/tbody/tr[4]/td/table/tbody/tr/td/table/tbody/tr[4]/td[2]/text()')
        get_data_in_db(username,rank,accepted)
        i+=1

def get_information_by_year():
    t1 = (datetime.datetime.now() - datetime.timedelta(days=365)).strftime('%Y-%m-%d %H:%M:%S')
    time = datetime.datetime.strptime(t1, "%Y-%m-%d %H:%M:%S")
    i = 0
    workbook = xlrd.open_workbook(r'name.xlsx')
    sheet1_name = workbook.sheet_names()[0]
    sheet1 = workbook.sheet_by_index(0)
    cols = sheet1.col_values(0)
    while (i < len(cols)):
        username = sheet1.row_values(i)[1]
        url = 'http://acm.hdu.edu.cn/userstatus.php?user=' + username
        driver.get(url)
        html = driver.page_source
        result=etree.HTML(html)
        accepted = result.xpath('/html/body/table/tbody/tr[4]/td/table/tbody/tr/td/table/tbody/tr[6]/td[2]/text()')
        elem=driver.find_element_by_css_selector('body > table > tbody > tr:nth-child(6) > td > table > tbody > tr > td > p:nth-child(7) > a:nth-child(3)')
        elem.click()
        html=driver.page_source
        j=1
        num=0
        while(num<int(accepted[0])):
            if (j == 17):
                next=driver.find_element_by_css_selector('#fixed_table > p > a:nth-child(3)')
                next.click()
                j=1
                j+=1
                continue
            html = driver.page_source
            result=etree.HTML(html)
            question=result.xpath('//*[@id="fixed_table"]/table/tbody/tr['+str(j)+']/td[2]/text()')
            if(question[0]=='Submit Time'):
                j+=1
                continue
            time1=datetime.datetime.strptime(question[0], "%Y-%m-%d %H:%M:%S")
            if(time<time1):
                num+=1
            else:
                break
            print(num)
            print(j)
            if(j!=1):
                j+=1
            else:
                pass
        get_data_in_CSV_by_year(username, num)
        i+=1

def get_information_by_month():
    t1 = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
    time = datetime.datetime.strptime(t1, "%Y-%m-%d %H:%M:%S")
    i = 0
    workbook = xlrd.open_workbook(r'name.xlsx')
    sheet1_name = workbook.sheet_names()[0]
    sheet1 = workbook.sheet_by_index(0)
    cols = sheet1.col_values(0)
    while (i < len(cols)):
        username = sheet1.row_values(i)[1]
        url = 'http://acm.hdu.edu.cn/userstatus.php?user=' + username
        driver.get(url)
        html = driver.page_source
        result=etree.HTML(html)
        accepted = result.xpath('/html/body/table/tbody/tr[4]/td/table/tbody/tr/td/table/tbody/tr[6]/td[2]/text()')
        elem=driver.find_element_by_css_selector('body > table > tbody > tr:nth-child(6) > td > table > tbody > tr > td > p:nth-child(7) > a:nth-child(3)')
        elem.click()
        html=driver.page_source
        j=1
        num=0
        while(num<int(accepted[0])):
            if (j == 17):
                next=driver.find_element_by_css_selector('#fixed_table > p > a:nth-child(3)')
                next.click()
                j=1
                j+=1
                continue
            html = driver.page_source
            result=etree.HTML(html)
            question=result.xpath('//*[@id="fixed_table"]/table/tbody/tr['+str(j)+']/td[2]/text()')
            if(question[0]=='Submit Time'):
                j+=1
                continue
            time1=datetime.datetime.strptime(question[0], "%Y-%m-%d %H:%M:%S")
            if(time<time1):
                num+=1
            else:
                break
            print(num)
            print(j)
            if(j!=1):
                j+=1
            else:
                pass
        get_data_in_CSV_by_month(username, num)
        i+=1

def get_information_by_day():
    t1 = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
    time = datetime.datetime.strptime(t1, "%Y-%m-%d %H:%M:%S")
    i = 0
    workbook = xlrd.open_workbook(r'name.xlsx')
    sheet1_name = workbook.sheet_names()[0]
    sheet1 = workbook.sheet_by_index(0)
    cols = sheet1.col_values(0)
    while (i < len(cols)):
        username = sheet1.row_values(i)[1]
        url = 'http://acm.hdu.edu.cn/userstatus.php?user=' + username
        driver.get(url)
        html = driver.page_source
        result=etree.HTML(html)
        accepted = result.xpath('/html/body/table/tbody/tr[4]/td/table/tbody/tr/td/table/tbody/tr[6]/td[2]/text()')
        elem=driver.find_element_by_css_selector('body > table > tbody > tr:nth-child(6) > td > table > tbody > tr > td > p:nth-child(7) > a:nth-child(3)')
        elem.click()
        html=driver.page_source
        j=1
        num=0
        while(num<int(accepted[0])):
            if (j == 17):
                next=driver.find_element_by_css_selector('#fixed_table > p > a:nth-child(3)')
                next.click()
                j=1
                j+=1
                continue
            html = driver.page_source
            result=etree.HTML(html)
            question=result.xpath('//*[@id="fixed_table"]/table/tbody/tr['+str(j)+']/td[2]/text()')
            if(question[0]=='Submit Time'):
                j+=1
                continue
            time1=datetime.datetime.strptime(question[0], "%Y-%m-%d %H:%M:%S")
            if(time<time1):
                num+=1
            else:
                break
            print(num)
            print(j)
            if(j!=1):
                j+=1
            else:
                pass
        get_data_in_CSV_by_day(username, num)
        i+=1

def main():
    #username='xgk1705xct'
    #get_information(username)
    #get_more(username)
    #get_all_information_in_db()
    get_information_by_year()
    get_information_by_month()
    get_information_by_day()

if __name__=='__main__':
    main()