from lxml import etree
from selenium import webdriver
driver=webdriver.Chrome("chromedriver.exe")

def get_url():
    url='https://www.gooood.cn/filter/type/all/country/all/material/all/office/all'
    driver.get(url)
    html=driver.page_source
    result=etree.HTML(html)
    p=result.xpath('//*[@id="wrapper"]/div/div/div/div/div/div[1]/div/div/div[3]/h2/a/text()')
    print(p)

def main():
    get_url()

if __name__=='__main__':
    main()