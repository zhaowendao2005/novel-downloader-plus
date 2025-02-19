import requests
from bs4 import BeautifulSoup
from request_chatper_url import RequestChapterURL
from chapter_downloader import ChapterDownloader

class NovelDownloader:
    def __init__(self, baseurl, url_path, output_file,selector_content,selector_chapter):
        self.baseurl = baseurl
        self.url_path = url_path
        self.output_file = output_file
        self.selector_content = selector_content
        self.selector_chatper = selector_chapter

    def download_chapters(self):
        requester = RequestChapterURL(self.baseurl, self.url_path, self.selector_chatper)
        chapters = requester.get_chapter_links_and_titles()

        chapter_contents = {}
        for chapter in chapters:
            chapter_url = chapter['url']
            chapter_title = chapter['title']
            Downloader = ChapterDownloader(chapter_url,self.selector_content)
            try:
                content = Downloader.get_chapter_content()
                chapter_contents[chapter_title] = content
                print(f"{chapter_title} 下载成功")
            except Exception as e:
                print(f"{chapter_title} 下载失败: {e}")

        self.save_to_file(chapter_contents)

    def save_to_file(self, chapter_contents):
        with open(self.output_file, 'w', encoding='utf-8') as f:
            for title, content in chapter_contents.items():
                f.write(f"{title}\n{content}\n\n")

if __name__ == '__main__':
    baseurl = "https://m.bqug8.com/"
    url_path = 'kan/37264/list.html'
    output_file = 'chapters_content.txt'
    selector_chapter = '.listmain a'
    selector_content = '#chaptercontent'
    downloader = NovelDownloader(baseurl, url_path, output_file,selector_chapter,selector_content)
    downloader.download_chapters()