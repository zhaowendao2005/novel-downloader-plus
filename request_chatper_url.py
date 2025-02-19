import requests
from bs4 import BeautifulSoup
class RequestChapterURL:
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {'User-Agent': user_agent}

    def __init__(self, baseurl,url_path,chatper_selector):

        self.baseurl=baseurl
        self.url = baseurl + url_path
        self.url_Path=url_path
        self.selector_chatper = chatper_selector


    def request_html(self):
        response = requests.get(self.url, headers=self.headers)
        if response.status_code == 200:
            return response.text
        else:
            response.raise_for_status()

    def get_chapter_links_and_titles(self):
        html = self.request_html()
        soup = BeautifulSoup(html, 'html.parser')
        chapters = []
        for link in soup.select(self.selector_chatper):
            title = link.get_text()
            href = link.get('href')
            if href and title:
                chapters.append({'title': title, 'url':baseurl.rstrip('/')+href})
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