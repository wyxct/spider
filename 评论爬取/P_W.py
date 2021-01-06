import requests
import re
import csv
import json
import pprint
import csv
import time
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
chrome_options = Options()
chrome_options.add_argument('--headless')
driver=webdriver.Chrome(chrome_options=chrome_options)

def get_url():
    csv_file=csv.reader(open('test1.csv','r'))
    for list in csv_file:
        url=list[11]
        print(url)
        driver.get(url)
        html=driver.page_source
        result=etree.HTML(html)
        t='//*[@id="react-project-comments"]/ul/li'
        # leader=result.xpath('//*[@id="react-project-header"]/div/div/div[2]/div/div[1]/div[2]/span/a/text()')
        # title=result.xpath('//*[@id="react-project-header"]/div/div/div[2]/div/div[1]/div[1]/h2/text()')
        # p=result.xpath('//*[@id="content-wrap"]/div[2]/section[1]/div/div/div/div/div[1]/div[2]/p/text()')
        # print(''.join(title))
        # print(''.join(p))
        try:
            n=result.xpath('//*[@id="comments-emoji"]/span/data/text()')
            if(''.join(n)!='0'):
                elem=driver.find_element_by_css_selector('#comments-emoji')
                elem.click()
                time.sleep(5)
                # html=driver.page_source
                # result=etree.HTML(html)
                # elem=driver.find_element_by_css_selector('#react-project-comments > ul > li:nth-child(2) > div.pl6.pt2 > div > button').click()
                html = driver.page_source
                result = etree.HTML(html)
                num = len(result.xpath(t))
                i=1
                for i in range(num+1):
                    j=1
                    first_name=result.xpath('//*[@id="react-project-comments"]/ul/li['+str(i)+']/div[1]/div[1]/div/span[1]/text()')
                    first_text=result.xpath('//*[@id="react-project-comments"]/ul/li['+str(i)+']/div[1]/div[2]/div/p/text()')
                    print(''.join(first_name))
                    print(''.join(first_text))
                    nums=len(result.xpath('//*[@id="react-project-comments"]/ul/li['+str(i)+']/div[2]/ul/li'))
                    for j in range(nums+1):
                        second_name=result.xpath('//*[@id="react-project-comments"]/ul/li['+str(i)+']/div[2]/ul/li['+str(j)+']/div/div[1]/div/span[1]/text()')
                        second_text=result.xpath('//*[@id="react-project-comments"]/ul/li['+str(i)+']/div[2]/ul/li['+str(j)+']/div/div[2]/div/p/text()')
                        print('        '+''.join(second_name))
                        print('        '+''.join(second_text))
            else:
                print("由于评论数为0，所以跳过该网页")
        except:
            print('该项目已经失效')


def main():
    get_url()

if __name__ == '__main__':
    main()