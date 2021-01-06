import requests
import os
import csv
import json
import xlrd
import time
import sys
from bs4 import BeautifulSoup
from lxml import etree
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
driver=webdriver.Chrome()


def get_data_in_CSV(username, rank, accepted):
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

class oj:
    def get_information(username):
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

    def get_condition(username):
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

    def get_all_information():
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

    def get_all_information_in_csv():
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

    def main():
        username='xgk1705xct'
        #get_information(username)
        #get_more(username)

    if __name__=='__main__':
        main()