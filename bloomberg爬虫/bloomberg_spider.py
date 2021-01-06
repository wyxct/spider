import re
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-automation'])
chrome_options = Options()
chrome_options.add_argument('--headless')
driver=webdriver.Chrome(options=options)

def search(name):
    j=1
    while(1):
        url='https://www.bloomberg.com/search?query='+name+'&page='+str(j)
        driver.get(url)
        html=driver.page_source
        result=etree.HTML(html)
        i=1
        while(i<=10):
            try:
                k=0
                topic=result.xpath('//*[@id="content"]/div/section/section[2]/section[1]/div[3]/div['+str(i)+']/article/div[1]/h1/a/text()')
                time=result.xpath('//*[@id="content"]/div/section/section[2]/section[1]/div[3]/div['+str(i)+']/article/div[1]/div[1]/span/time/text()')
                m=time[0][1:4]
                y=time[0][-5:-1]
                print(m)
                print(y)
                if(m=='Mar' and y=='2019'):
                    n=''.join(topic)+'    '+time[0]
                    out = open(name+'.txt', 'a', newline='')
                    out.write(n + '\r\n')
                i+=1
            except:
                print('标题已经获取完毕，或者出现连接错误')
                return
        j+=1

# def main():
#     search('nike')
#
# if  __name__=='__main__':
#     main()

class chaxun:
    def find(name):
        search(name)
