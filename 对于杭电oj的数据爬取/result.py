import csv
import xlrd
from lxml import etree
from selenium import webdriver
opt = webdriver.ChromeOptions()
opt.set_headless() #设置driver配置为无头模式
driver=webdriver.Chrome(options=opt)


def get_data_in_CSV(username, rank, accepted):     #将数据放入CSV格式文件中
    i = 0
    t = 0
    all = []
    all.append(username)
    all.append(rank)  #数据存到数组里面用来存到csv里面，因为写入需要用数组才能写成一排
    all.append(accepted)
    # print(all)
    out = open('oj' + '.csv', 'a', newline='') #读取oj.csv
    csv_write = csv.writer(out, dialect='excel')
    csv_write.writerow(all)
    print('生成csv文件成功!')

def get_all_information_in_csv():      #根据文件目录下的CSV文件，读取其中的姓名和用户名来生成一个刷题报表，存入CSV中
    i=0
    workbook = xlrd.open_workbook(r'name.xlsx')#打开name.csv这个文件
    sheet1_name = workbook.sheet_names()[0]
    sheet1 = workbook.sheet_by_index(0)
    cols=sheet1.col_values(0)  #读取里面的每一行
    while(i<len(cols)):   #按出现的每一行循环读取和写入
        username = sheet1.row_values(i)[1]
        url = 'http://acm.hdu.edu.cn/userstatus.php?user=' + username #进入这个用户名的页面
        driver.get(url)    #这里用的是selenium的webdriver读取的网页源码
        html = driver.page_source
        # print(html)
        result = etree.HTML(html)  #转成HTML格式的文字
        username = result.xpath('/html/body/table/tbody/tr[4]/td/table/tbody/tr/td/h1/text()')
        rank = result.xpath('/html/body/table/tbody/tr[4]/td/table/tbody/tr/td/table/tbody/tr[2]/td[2]/text()')   #用xpath定位数据位置
        accepted = result.xpath('/html/body/table/tbody/tr[4]/td/table/tbody/tr/td/table/tbody/tr[4]/td[2]/text()')
        get_data_in_CSV(username[0].replace('\xa0',' '),rank[0],accepted[0])   #写入oj.csv 文件中
        i+=1

def main():
    get_all_information_in_csv()

if __name__=='__main__':
    main()