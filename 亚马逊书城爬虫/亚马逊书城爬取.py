import requests
from lxml import etree,html
from selenium import webdriver
import re
import json
import xlwt

driver=webdriver.Chrome('chromedriver.exe')

def get_url():
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('sheet1')
    worksheet.write(0, 0, label='标题')
    worksheet.write(0, 1, label='作者')
    worksheet.write(0, 2, label='评分')
    worksheet.write(0, 3, label='评论人数')
    worksheet.write(0, 4, label='价格')
    n=1
    i=1
    while i<=63:
        driver.get('https://www.amazon.cn/s?k=python&i=stripbooks&__mk_zh_CN=亚马逊网站&page='+str(i))
        html_data=driver.page_source
        selector = html.fromstring(html_data)
        all=selector.xpath('//*[@id="search"]/div[1]/div[2]/div/span[4]/div[1]/div')
        for one in all:
            title=one.xpath('./div/span/div/div/div[2]/div[2]/div/div[1]/div/div/div[1]/h2/a/span/text()') if len(one.xpath('./div/span/div/div/div[2]/div[2]/div/div[1]/div/div/div[1]/h2/a/span/text()'))>0 else "无"
            writer=one.xpath('./div/span/div/div/div[2]/div[2]/div/div[1]/div/div/div[1]/div/span[2]/text()') if len(one.xpath('./div/span/div/div/div[2]/div[2]/div/div[1]/div/div/div[1]/div/span[2]/text()'))>0 else "无"
            score=one.xpath('./div/span/div/div/div[2]/div[2]/div/div[1]/div/div/div[2]/div/span[1]/span/a/i[1]/span/text()') if len(one.xpath('./div/span/div/div/div[2]/div[2]/div/div[1]/div/div/div[2]/div/span[1]/span/a/i[1]/span/text()'))>0 else "无"
            c_p=one.xpath('./div/span/div/div/div[2]/div[2]/div/div[1]/div/div/div[2]/div/span[2]/a/span/text()') if len(one.xpath('./div/span/div/div/div[2]/div[2]/div/div[1]/div/div/div[2]/div/span[2]/a/span/text()'))>0 else "无"
            price=one.xpath('./div/span/div/div/div[2]/div[2]/div/div[2]/div[1]/div/div[1]/div[2]/div/a/span/span[1]/text()') if len(one.xpath('./div/span/div/div/div[2]/div[2]/div/div[2]/div[1]/div/div[1]/div[2]/div/a/span/span[1]/text()'))>0 else "无"
            if(title[0]=="无" and writer[0]=="无" and score[0]=="无" and c_p[0]=="无" and price[0]=="无"):
                pass
            else:
                print(title[0] + '   ' + writer[0] + '   ' + score[0] + '   ' + c_p[0] + '   ' + price[0])
                worksheet.write(n, 0, label=title[0])
                worksheet.write(n, 1, label=writer[0])
                worksheet.write(n, 2, label=score[0])
                worksheet.write(n, 3, label=c_p[0])
                worksheet.write(n, 4, label=price[0])
                workbook.save('amazon_books.csv')
                n+=1
        i+=1

def main():
    get_url()

if __name__ == '__main__':
    main()