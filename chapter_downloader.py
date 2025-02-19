import requests
from bs4 import BeautifulSoup
import os
from request_chatper_url import RequestChapterURL


class ChapterDownloader:
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {'User-Agent': user_agent}
    selector = '#chaptercontent'
    def __init__(self, chapter_url, selector):
        self.chapter_url = chapter_url
        self.selector = selector
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
        for chapter_conents in soup.select(selector):
            title_contents.append(chapter_conents.get_text())
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