import requests
import json
import re
import csv
from selenium import webdriver
from bs4 import BeautifulSoup
from lxml import etree

driver=webdriver.Chrome()

def get_form(url):
    data=['Qualified for the November debate','NATIONAL POLLING AVERAGE','INDIVIDUAL CONTRIBUTIONS','WEEKLY NEWS COVERAGE']
    write(data)
    driver.get(url)
    elem=driver.find_element_by_css_selector('#democratic-polls > div.g-graphic.g-graphic-freebird > div.g-item.g-overview > div.g-item.g-graphic.g-candidate-overview > div > div.g-candidates-table-outer.g-table-outer > table > tbody > tr.g-cand-rollup > td')
    driver.execute_script('arguments[0].click()', elem)
    html = driver.page_source
    bs=BeautifulSoup(html,'html.parser')
    bs1=bs.find('div',class_='g-item g-overview').find('tbody')
    rows=bs1.find_all('tr')
    for row in rows:
        try:
            data=[]
            cols=row.find_all('td')
            data.append(cols[0].find('span',class_='g-desktop').get_text())
            data.append(cols[1].find('span',class_='g-contents').get_text())
            data.append(cols[2].find('span',class_='g-contents').get_text())
            data.append(cols[3].find('span',class_='g-contents').get_text())
            write(data)
        except:
            break

def write(data):
    file=open('data.csv','a',newline='')
    content = csv.writer(file, dialect='excel')
    content.writerow(data)

def main():
    url="https://www.nytimes.com/interactive/2020/us/elections/democratic-polls.html"
    get_form(url)

if __name__ == '__main__':
    main()