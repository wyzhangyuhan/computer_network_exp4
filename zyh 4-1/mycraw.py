import re
import time
import requests
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup

#可根据关键词对新闻网页中的新闻进行爬取
class craw_web:
    def __init__(self, url, keywords):
        self.url = url
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75'}
        self.webtext = ''
        self.keywords = keywords


    def gethtml(self): # 获取网页文本信息(html)
        r =  requests.get(self.url, headers=self.headers)
        r.encoding = 'utf-8'
        self.webtext = r.text
        #写到本地
        with open('./craw/sina.html', 'w', encoding='utf-8', errors='ignore') as fp:
            fp.write(self.webtext)
        print('保存成功')
    
    def isnews(self, mystr):
        try:
            d = mystr.split('/')
            if '.html' in d[-1] or '.shtml' in d[-1]:
                ex = '^\d{4}-\d{1,2}-\d{1,2}'
                for tmp in d:
                    if re.match(ex, tmp) != None:
                        # print('是新闻')
                        return True
            return False
        except Exception as e:
            return False


    def getlink(self):
        soup = BeautifulSoup(self.webtext,'html.parser')
        #新闻网站中的新闻通常有外部链接可通过<a>来下载
        a_list = soup.find_all('a') #找到所有的a标签
        a_list = list(set(a_list)) # 通过set去重
        # a_list.remove('')
        a_list = a_list[0:1000]  #新浪新闻几千多条新闻懒得等，就取了1000条
        if len(a_list) == 0:
            print('爬取失败.')

        link = []
        title = []
        date = []
        print('开始爬取新闻：')
        for a in tqdm(a_list):
            tp_link = a.get('href')
            if self.isnews(tp_link):
                d = tp_link.split('/')
                riqi = ''
                ex = '^\d{4}-\d{1,2}-\d{1,2}'
                for tmp in d:
                    if re.match(ex, tmp) != None:
                        riqi = tmp
                if not self.keywords in a.text: #若不包含新闻关键词，跳过
                    a_list.remove(a)
                    time.sleep(0.01)
                    continue          
                link.append(tp_link)
                title.append(a.text)
                date.append(riqi)
                time.sleep(0.01)
            else:
                time.sleep(0.011)
                continue                   
        print('爬取新闻结束！')
        news = pd.DataFrame({
            'title': title,
            'link': link,
            'date': date
        })
        print(news)
        news.to_excel('./craw/news.xls',encoding='utf-8', index=True, header=True)



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
                    img = self.url + img
                img_binary = requests.get(img, headers=self.headers).content # 补充协议头

                file_name = img.split('/')[-1] # 获取图片文件名
                file_name = file_name.split('?')[0]

                with open(f'./craw/{file_name}', 'wb') as fp:
                    fp.write(img_binary)
                # print(file_name, '，下载成功')
                success_count += 1
                time.sleep(1)
            except Exception as e:
                print(e)
                error_count += 1
            continue
        print('下载图片结束！')
        print(f'总计下载：{success_count}，下载失败：{error_count}')


if __name__ == '__main__':
    url = 'https://news.sina.com.cn/'
    keywords = '印度'
    cw = craw_web(url,keywords)
    cw.gethtml() #爬取网页文本
    cw.getlink()
    # cw.download_img() #爬取网页图片
    
    