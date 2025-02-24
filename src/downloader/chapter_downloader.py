import requests
from bs4 import BeautifulSoup
import os
from .request_chatper_url import RequestChapterURL
import random
import logging

class ChapterDownloader:
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


    headers = {
        'User-Agent': random.choice(agent_list)
    }
    selector = '#chaptercontent'
    def __init__(self, chapter_url, selector):
        self.chapter_url = chapter_url
        self.selector = selector
    def getrandomagent(self):
        return random.choice(self.agent_list)

    def request_html(self):
        try:
            response = requests.get(self.chapter_url,
                                    headers=self.headers,
                                    timeout=(3, 10))  # 连接3秒，读取10秒超时
            response.raise_for_status()
            return response.text
        except requests.exceptions.Timeout:
            logging.warning(f"请求超时: {self.chapter_url}")
            raise
        except requests.exceptions.RequestException as e:
            logging.warning(f"网络请求失败: {str(e)}")
            raise


    def request_html(self):
        response = requests.get(self.chapter_url, headers=self.headers)
        if response.status_code == 200:
            return response.text
        else:
            response.raise_for_status()

    def get_chapter_content(self):
        html = self.request_html()
        soup = BeautifulSoup(html, 'html.parser')
        title_contents= []
        for chapter_contents in soup.select(self.selector):
            title_contents.append(chapter_contents.get_text())
        #for i in chapter_conents:
         #   print(i)
        #chapter_conents转化为字符串
        if '<br/>' in title_contents:
            title_contents.remove('<br/>')
        if "<br>" in title_contents:
            title_contents.remove("<br>")
        finallyChapterContent = '\n'.join(title_contents)
        #print(finallyChapterContent)
        return finallyChapterContent





if __name__ == '__main__':
    chapter_url = 'https://m.bqug8.com/kan/37264/1.html'
    selector=('#chaptercontent')
    downloader = ChapterDownloader(chapter_url,selector)
    content = downloader.get_chapter_content()
    # 章节内容保存至文件
    with open('chapter.txt', 'w', encoding='utf-8') as f:
        f.write(content)


"""
chapter_url 写章节内容链接
selector填章节内容的类或者id，类#id.



"""