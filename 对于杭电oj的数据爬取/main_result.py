import requests
import os
import csv
import json
import xlrd
import time
import re
# import MySQLdb
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

def crawl_coder_status(username):      #得到杭电的刷题基础信息
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

def crawl_condition(username):      #得到杭电刷题的每题提交量和通过次数
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
    print(str(t))

def crawl_all_coder_status():      #根据文件目录下的CSV文件，读取其中的姓名和用户名来生成一个刷题报表
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

def crawl_all_information_and_put_in_db():      #根据文件目录下的CSV文件，读取其中的姓名和用户名来生成一个刷题报表，存入数据库中
    i=0
    username=[]
    rank=[]
    accepted=[]
    workbook = xlrd.open_workbook(r'name.xlsx')
    sheet1_name = workbook.sheet_names()[0]
    sheet1 = workbook.sheet_by_index(0)
    cols=sheet1.col_values(0)
    while(i<len(cols)):
        username1 = sheet1.row_values(i)[1]
        url = 'http://acm.hdu.edu.cn/userstatus.php?user=' + username1
        driver.get(url)
        html = driver.page_source
        # print(html)
        result = etree.HTML(html)
        username1 = result.xpath('/html/body/table/tbody/tr[4]/td/table/tbody/tr/td/h1/text()')
        rank1 = result.xpath('/html/body/table/tbody/tr[4]/td/table/tbody/tr/td/table/tbody/tr[2]/td[2]/text()')
        accepted1 = result.xpath('/html/body/table/tbody/tr[4]/td/table/tbody/tr/td/table/tbody/tr[4]/td[2]/text()')
        username.append(username1[0])
        rank.append(rank1[0])
        accepted.append(accepted1[0])
        i+=1
    date = {'username': username, 'rank': rank, 'accepted': accepted}
    date = pd.DataFrame(date)
    print(date)
    # date.to_sql('oj', con=dbcon, flavor='mysql')

def crawl_information_by_time_and_put_in_db(t):     #获取每年内分组内的同学的刷题数并排名并存入数据库中
    if (t == 'year'):
        tt = 365
    if (t == 'month'):
        tt = 30
    if (t == 'week'):
        tt = 7
    t1 = (datetime.datetime.now() - datetime.timedelta(days=tt)).strftime('%Y-%m-%d %H:%M:%S')
    time = datetime.datetime.strptime(t1, "%Y-%m-%d %H:%M:%S")
    i = 0
    workbook = xlrd.open_workbook(r'name.xlsx')
    sheet1_name = workbook.sheet_names()[0]
    sheet1 = workbook.sheet_by_index(0)
    cols = sheet1.col_values(0)
    username1=[]
    num1=[]
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
            if(j!=1):
                j+=1
            else:
                pass
        username1.append(username)
        num1.append(num)
        i+=1
    data={'username':username1,'number':num1}
    data = pd.DataFrame(data)
    data1=data.sort_values(by="number",ascending=False)
    print(data1)
    # data1.to_sql('oj', con=dbcon, flavor='mysql')

def crawl_coder_problem_status(pid,username):    #可根据题号和用户名对此题该用户的答题情况做出规整
    Judge_statu=[]
    url='http://acm.hdu.edu.cn/status.php?first=&pid='+pid+'&user='+username+'&lang=0&status=0'
    driver.get(url)
    html=driver.page_source
    result=etree.HTML(html)
    ID=result.xpath('//*[@id="fixed_table"]/table/tbody/tr/td[1]/text()')
    # print(ID)
    Submit_time=result.xpath('//*[@id="fixed_table"]/table/tbody/tr/td[2]/text()')
    # print(Submit_time)
    b = BeautifulSoup(html, 'lxml').find('table', align="center").find('div', id="fixed_table").find_all('tr')
    for i in b:
        bb = i.find_all('td')
        Judge_statu.append(bb[2].get_text())
    # print(Judge_statu)
    Problem_id=['Problem_id']+result.xpath('//*[@id="fixed_table"]/table/tbody/tr/td[4]/a/text()')
    # print(Problem_id)
    Exe_time=result.xpath('//*[@id="fixed_table"]/table/tbody/tr/td[5]/text()')
    # print(Exe_time)
    Exe_memory=result.xpath('//*[@id="fixed_table"]/table/tbody/tr/td[6]/text()')
    # print(Exe_memory)
    Code_len=result.xpath('//*[@id="fixed_table"]/table/tbody/tr/td[7]/text()')
    # print(Code_len)
    language=result.xpath('//*[@id="fixed_table"]/table/tbody/tr/td[8]/text()')
    # print(language)
    all={'ID':ID,'Submit_time':Submit_time,'Judge_statu':Judge_statu,'Problem_id':Problem_id,'Exe_time':Exe_time,'Exe_memory':Exe_memory,'Code_len':Code_len,'language':language}
    data=pd.DataFrame(all)
    print(data)

def main():
    username='xgk1705xct'
    crawl_condition('xgk1705xct')

if __name__=='__main__':
    main()