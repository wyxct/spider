import requests
import re
import os
import threading

def get_html(url):
    html=requests.get(url)
    return html.text

def get_hrefs(page):
    reg= "href=\"(.+?)\""
    hrefs=[]
    urlre = re.compile(reg)
    urllist = urlre.findall(page)
    for url in urllist:
        href='http://www.feimax.com'+url
        hrefs.append(href)
    # print(hrefs)
    return hrefs

def get_img(page): #Find a picture on the page and download it
    pics = []
    img="src=\"(.+?)\""
    imgre = re.compile(img)
    imgs = imgre.findall(page)
    srcs=[] #List of pages where pictures are stored
    names=[] #Picture name list
    for img in imgs:
        try: #Because the wrong picture is not the picture of this website, write a try to ignore the error
            src='http://www.feimax.com'+img
            src2 = src[src.rfind("/"):]#Get the last / following text
            name=src2.split('/')#Removal /
            pics.append(src)
        except:
            continue
    t = threading.Thread(target=download_img(pics))  # New thread download picture
    t.start()

def download_img(pics):#Download pictures
    for src in pics:
        s = requests.Session()
        r = s.get(src)
        name=src.split('http://')
        src2 = src[src.rfind("/"):]
        path_name=name[1].split(src2)
        isExists = os.path.exists("./imgs/"+path_name[0])
        if not isExists:
            path="./imgs/"+path_name[0]
            path=path.replace('/','\\')
            os.makedirs(path)
            f = open("./imgs/" + name[1], 'wb')
            f.write(r.content)
            f.close()
            print(src2+"已经下载完成")
        else:
            isExists1 = os.path.exists("./imgs/" + name[1])
            if not isExists1:
                f = open("./imgs/" + name[1], 'wb')
                f.write(r.content)
                f.close()
                print(src2+"已经下载完成")

def get_again(hrefs,depth):#Depth specifies the depth for the user, which must be greater than or equal to 1
    # print(hrefs)
    hrefs_A=[]
    if(depth>1):
        for href in hrefs:#Loop through each link
            page=get_html(href)
            get_img(page)
            hrefs_A=get_hrefs(page)
            get_again(hrefs_A, depth-1)  # Recursively handle next depth

def put_depth(url,depth):#Depth specifies the depth for the user, which must be greater than or equal to 1
    page=get_html(url)
    hrefs=get_hrefs(page)
    # print(hrefs)
    get_again(hrefs,depth)

def main():
    url="http://www.feimax.com/images"
    # page=get_html(url)
    # get_hrefs(page)
    # get_img(page)
    put_depth(url, 4)

if __name__ == '__main__':
    main()