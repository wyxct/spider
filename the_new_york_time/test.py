import requests
import json
import pandas as pd
import re
import csv
from selenium import webdriver
from bs4 import BeautifulSoup
from lxml import etree

driver=webdriver.Chrome()

def get_form(url):
    # data=['Qualified for the November debate','NATIONAL POLLING AVERAGE','INDIVIDUAL CONTRIBUTIONS','WEEKLY NEWS COVERAGE']
    # write(data)
    nam=[]
    nat=[]
    ind=[]
    wee=[]
    driver.get(url)
    elem=driver.find_element_by_css_selector('#democratic-polls > div.g-graphic.g-graphic-freebird > div.g-item.g-overview > div.g-item.g-graphic.g-candidate-overview > div > div.g-candidates-table-outer.g-table-outer > table > tbody > tr.g-cand-rollup > td')
    driver.execute_script('arguments[0].click()', elem)
    html = driver.page_source
    bs=BeautifulSoup(html,'html.parser')
    bs1=bs.find('div',class_='g-item g-overview').find('tbody')
    rows=bs1.find_all('tr')
    for row in rows:
        try:
            # data=[]
            cols=row.find_all('td')
            nam.append(cols[0].find('span',class_='g-desktop').get_text())
            nat.append(cols[1].find('span',class_='g-contents').get_text())
            ind.append(cols[2].find('span',class_='g-contents').get_text())
            wee.append(cols[3].find('span',class_='g-contents').get_text())
            # write(data)
        except:
            break
    dict={'Qualified for the November debate':nam,'NATIONAL POLLING AVERAGE':nat,'INDIVIDUAL CONTRIBUTIONS':ind,'WEEKLY NEWS COVERAGE':wee}
    dataf=pd.DataFrame(dict)
    print(dataf)
    return dict

def get_num(dict):
    nam1 = []
    nat1 = []
    ind1 = []
    wee1 = []
    for name in dict['Qualified for the November debate']:
        nam1.append(name)

    for num in dict['NATIONAL POLLING AVERAGE']:
        result = re.findall(r"\d+\.?\d*", num)
        nat1.append(result[0])

    for num in dict['INDIVIDUAL CONTRIBUTIONS']:
        result = re.findall(r"\d+\.?\d*", num)
        ind1.append(result[0])

    for num in dict['WEEKLY NEWS COVERAGE']:
        result = re.findall(r"\d+\.?\d*", num)
        wee1.append(result[0])
    dict = {'Qualified for the November debate': nam1, 'NATIONAL POLLING AVERAGE': nat1,
            'INDIVIDUAL CONTRIBUTIONS': ind1, 'WEEKLY NEWS COVERAGE': wee1}
    dataf = pd.DataFrame(dict)
    print(dataf)

# def write(data):
#     file=open('data.csv','a',newline='')
#     content = csv.writer(file, dialect='excel')
#     content.writerow(data)

def main():
    url="https://www.nytimes.com/interactive/2020/us/elections/democratic-polls.html"
    data=get_form(url)
    get_num(data)

if __name__ == '__main__':
    main()