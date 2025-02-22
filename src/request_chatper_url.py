import requests
from bs4 import BeautifulSoup
import logging
class RequestChapterURL:

    def __init__(self, baseurl, url_path, selector_chapter):
        self.baseurl = baseurl
        self.url_path = url_path
        self.selector_chapter = selector_chapter
        agent_list = [
            "Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
            "Avant Browser/1.2.789rel1 (http://www.avantbrowser.com)",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5",
            "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7",
            "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
            "Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10"
        ]
        import random
        self.headers = {
            'User-Agent': random.choice(agent_list)
        }


    def request_html(self):
        response = requests.get(self.url, headers=self.headers)
        if response.status_code == 200:
            return response.text
        else:
            response.raise_for_status()

    def get_chapter_links_and_titles(self):
        try:
            response = requests.get(self.baseurl + self.url_path,headers=self.headers)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 403:
                logging.error("访问被禁止 (403 Forbidden): 请检查是否被网站屏蔽")
            else:
                logging.error(f"HTTP错误: {http_err}")
            return []
        except requests.exceptions.RequestException as req_err:
            logging.error(f"请求错误: {req_err}")
            return []
        soup = BeautifulSoup(response.content, 'html.parser')
        chapters = []
        for link in soup.select(self.selector_chapter):
            title = link.get_text(strip=True)
            href = link.get('href')
            chapters.append({'title': title, 'url': self.baseurl.rstrip('/') + href})
        return chapters
if __name__ == '__main__':# 使用示例
    baseurl = "https://m.bqug8.com/"
    url_path='kan/37264/list.html'
    selector = '.listmain a'

    requester = RequestChapterURL(baseurl,url_path,selector)
    chapters = requester.get_chapter_links_and_titles()
    # 章节信息保存至文件
    with open('chapters.txt', 'w', encoding='utf-8') as f:
        for chapter in chapters:
            f.write(f"{chapter['title']} {chapter['url']}\n")