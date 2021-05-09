import re
import os
import time
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup

class craw_web:
    def __init__(self, url):
        self.url = url
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75'}
        self.webtext = ''


    def gethtml(self): # 获取网页文本信息(html)
        r =  requests.get(self.url, headers=self.headers)
        r.encoding = 'utf-8'
        self.webtext = r.text
        # print(self.webtext)
        #写到本地
        with open('./img/szu.html', 'w', encoding='utf-8', errors='ignore') as fp:
            fp.write(self.webtext)
        print('保存成功')

    def gettext(self): # 获取网页内所有的文字信息
        soup = BeautifulSoup(self.webtext,'html.parser')
        content = soup.get_text()
        with open('./img/szu.txt', 'w', encoding='utf-8', errors='ignore') as fp:
            fp.write(self.webtext)

    def getcss(self):
        soup = BeautifulSoup(self.webtext,'html.parser')
        link_list = soup.find_all('link')

        for i in link_list():
            tmp_css = i.get('herf')

    def getlink(self):
        error_count = 0
        success_count = 0
        soup = BeautifulSoup(self.webtext,'html.parser')

        
        a_list = soup.find_all('a') #找到所有的a标签
        a_list = list(set(a_list)) # 通过set去重
        # a_list.remove('')
        print(a_list)

        if len(a_list) == 0:
            print('爬取失败.')

        print('开始下载外部连接：')
        content = [] 
        for a in tqdm(a_list):
        # for a in a_list:
            try:
                a = self.url + a.get('href')
                content.append(a)
                success_count += 1
                time.sleep(1)
            except Exception as e:
                print(e)
                error_count += 1
            continue
        with open('./img/link.txt', 'w') as fp:
            fp.write(content)
        print('下载外链结束！')
        print(f'总计下载：{success_count}，下载失败：{error_count}')

    def download_media(self): #获取网页中视频媒体等信息
        error_count = 0
        success_count = 0
        
        ex = '<video.*?src="(.*?)".*?' #匹配视频格式，获取视频链接
        mea_list = re.findall(ex, self.webtext)
        mea_list = list(set(mea_list)) # 通过set去重
       
        if len(mea_list) == 0:
            print('爬取失败.')

        print('开始下载视频：')
        for mea in tqdm(mea_list):
        # for img in img_list:
            try:
                if not (mea.startswith('http') or mea.startswith('https')): # 填充视频链接
                    mea = 'https://www.szu.edu.cn/' + mea
                mea_binary = requests.get(mea, headers=self.headers).content # 补充协议头

                file_name = mea.split('/')[-1] # 获取视频文件名
                file_name = file_name.split('?')[0]

                with open(f'./img/{file_name}', 'wb') as fp:
                    fp.write(mea_binary)
                # print(file_name, '，下载成功')
                success_count += 1
                time.sleep(1)
            except Exception as e:
                print(e)
                error_count += 1
            continue
        print('下载视频结束！')
        print(f'总计下载：{success_count}，下载失败：{error_count}')


    def download_img(self): #下载网页上的图片信息
        error_count = 0
        success_count = 0
        
        ex = '<img.*?src="(.*?)".*?' #匹配图片格式，获取图片链接
        img_list = re.findall(ex, self.webtext)
        img_list = list(set(img_list)) # 通过set去重
        img_list.remove('')
        # print(len(img_list))
        # print('图片地址:', img_list)
        if len(img_list) == 0:
            print('爬取失败.')
        print('开始下载图片：')
        for img in tqdm(img_list):
        # for img in img_list:
            try:
                if not (img.startswith('http') or img.startswith('https')): # 填充图片链接
                    if img[0]!= '/':
                        tmp_img = '/' + img
                    else:
                        tmp_img = img
                    img = 'https://www.szu.edu.cn/' + img
                img_binary = requests.get(img, headers=self.headers).content # 补充协议头

                tmp_list = tmp_img.split('/')
                file_name = img.split('/')[-1] # 获取图片文件名
                file_name = file_name.split('?')[0]
                path = './img'
                for i in range(len(tmp_list) -1):
                    path = path + tmp_list[i] + '/'

                # print(path)
                if not os.path.exists(path):
                    os.makedirs(path)
                with open(f'{path}{file_name}', 'wb') as fp:
                    fp.write(img_binary)
                # print(file_name, '，下载成功')
                success_count += 1
                time.sleep(0.1)
            except Exception as e:
                print(e)
                error_count += 1
            continue
        print('下载图片结束！')
        print(f'总计下载：{success_count}，下载失败：{error_count}')


    def get_dir_size(self):
        size = 0
        dir = '../'
        for root, dirs, files in os.walk(dir):
            size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
        return size


if __name__ == '__main__':
    url = 'https://www.szu.edu.cn/'
    cw = craw_web(url)
    cw.gethtml() #爬取网页文本
    # cw.getlink()
    # cw.gettext()
    cw.download_img() #爬取网页图片
    # cw.download_media() #爬取网页视频
    size = cw.get_dir_size()
    print('Total size is: %.3f Mb'%(size/1024/1024))