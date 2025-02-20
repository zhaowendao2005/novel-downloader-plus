import requests
from bs4 import BeautifulSoup
import logging
class RequestChapterURL:
    def __init__(self, baseurl, url_path, selector_chapter):
        self.baseurl = baseurl
        self.url_path = url_path
        self.selector_chapter = selector_chapter


    def request_html(self):
        response = requests.get(self.url, headers=self.headers)
        if response.status_code == 200:
            return response.text
        else:
            response.raise_for_status()

    def get_chapter_links_and_titles(self):
        try:
            response = requests.get(self.baseurl + self.url_path)
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