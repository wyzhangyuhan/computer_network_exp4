'''
Author: your name
Date: 2021-04-07 09:11:09
LastEditTime: 2021-04-09 10:46:37
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \4-1\geturlres.py
'''
import urllib3
import bs4
import os
import time
from typing import List, NoReturn

class Crawler:
    def __init__(self, url=None, name="apple"):
        self.http = urllib3.PoolManager()
        self.htmlCache = None
        self.url = url
        self.user_agent   = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.63"
        self.req_headers  = {"User-Agent": self.user_agent}

        # set folder
        self.image_folder = f"./image__{name}/"
        self.html_folder  = f"./html_text__{name}/"     
        
        # create the folder
        if not os.path.exists(self.image_folder):
            os.mkdir(self.image_folder)
        if not os.path.exists(self.html_folder):
            os.mkdir(self.html_folder)

    def get_html(self):
        # request from url
        r = self.http.request("GET", self.url, headers=self.req_headers)

        # get html text and encode with utf-8
        self.htmlCache = r.data.decode("utf-8", "ignore")

        # save html file
        with open(self.html_folder + "index.html", "w", encoding="utf-8") as f:
            f.write(self.htmlCache)
        return self.htmlCache

    def get_images(self):
        if self.htmlCache == None:
            self.get_html()
        
        # Beautiful soup is delicious
        soup = bs4.BeautifulSoup(self.htmlCache, "html.parser")

        # find all img tags
        img_list = soup.find_all("img")
        
        # remove the duplications.
        imgs = set(img_list)
        image_set = set()
        for each in imgs:
            src = each.get("src")
            if src.strip() == "":
                image_set.add(src)

        # the index of image
        ind = 0
        for image_url in image_set:
            # request from server
            r = self.http.request("GET", self.url + "/" + image_url, headers=self.req_headers)
            img_bin = r.data

            # the file suffix, such as "png", "jpg"
            try:
                suffix = image_url.split(".")[-1]
            except Exception as e:
                print(e)
                print(f'parsing image file "{image_url}" failed.')
                continue
            
            # save the file
            with open(f"{self.image_folder}{ind}.{suffix}", "wb") as fp:
                fp.write(img_bin)
            print(image_url)
            
            # avoid high-frequent requests and be denied 
            time.sleep(0.8)

            # notification and update
            print(f"{ind}: download successfully")
            ind += 1
        
        # print result
        print("summary: %d success, %d failed, complete %f%%." %
              (ind, len(image_set)-ind, 100*ind/len(image_set)))

class DoubanCrawler(Crawler):
    def __init__(self):
        url = "https://movie.douban.com/top250"
        Crawler.__init__(self, url)
        self.get_html()
    
    def get_movie_each_page(self, html, rank_threshold=10):
        soup = bs4.BeautifulSoup(html, "html.parser")

        # return result
        rtn = []

        # find the big frame of the movie's grid view
        frame = soup.find("ol", class_="grid_view")

        # all movies lie under "li" tag
        movies_info_this_page = frame.find_all("li")
        for movie in movies_info_this_page:
            # get movie's name and rank
            movie_div_tag  = movie.find("div", class_="hd")
            movie_rank_tag = movie.find("span", class_="rating_num")
            movie_name = movie_div_tag.a.span.text
            movie_rank = movie_rank_tag.text

            # check the rank to determine description
            description = "Unshown"
            rank = float(movie_rank)
            
            # if greater than threshold, then get detail description
            if rank > rank_threshold:
                # go into detailed page
                url_in = movie_div_tag.a.get("href")
                r = self.http.request("GET", url_in, headers=self.req_headers)
                html_in = r.data.decode("utf-8", "ignore")

                # find the description
                soup = bs4.BeautifulSoup(html_in, "html.parser")
                content = soup.find("span", property="v:summary")
                description = content.text
                description = "".join(description.split())
                description = "".join(description.split('\n'))

            # fill entry of movie list
            rtn.append(f"{movie_name}, {movie_rank}, {description}\n")
            time.sleep(0.08)
        
        return rtn

    def get_all_movies(self, threshold_rank):
        # html and url will change within each iteration
        html = self.htmlCache
        url  = self.url

        # total information of all movies
        movies_info = ["MOVIE, RANK, DESCRIPTION\n"]
        n_page = 1
        while True:
            movies_info.extend(self.get_movie_each_page(html, threshold_rank))
            soup = bs4.BeautifulSoup(html, "html.parser")
            next_page = soup.find("span", class_="next")
            # if next page exists
            if not next_page.a is None:
                link = next_page.a.get("href")
                url  = self.url + link
                r = self.http.request("GET", url, headers=self.req_headers)
                html = r.data.decode("utf-8", "ignore")
            else:
                break
            
            # sleep to avoid being denied
            time.sleep(0.2)

            # notification
            print(f"Complete page {n_page}")
            n_page += 1
        
        print("Complete page 10")

        # save csv file
        with open("douban_Top250.csv", "w", encoding="utf-8") as f:
            for each_movie in movies_info:
                f.write(each_movie)

if __name__ == "__main__":
    c = Crawler("https://www.szu.edu.cn")
    c.get_images()

    # dc = DoubanCrawler()
    # dc.get_all_movies(9.4)
    # dc.get_movie_each_page(dc.htmlCache)