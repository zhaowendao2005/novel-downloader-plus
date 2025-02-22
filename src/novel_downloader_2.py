import requests
from bs4 import BeautifulSoup
import logging
import traceback
import time
from request_chatper_url import RequestChapterURL
from chapter_downloader import ChapterDownloader
from async_downloader import AsyncChapterDownloader

# 配置日志系统
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('../novel_downloader.log'),
        logging.StreamHandler()
    ]
)


class NovelDownloader:
    def __init__(self, baseurl, url_path, output_file, selector_content, selector_chapter,max_workers=8):
        self.baseurl = baseurl
        #默认线程数为8
        self.url_path = url_path
        self.output_file = output_file
        self.selector_content = selector_content
        self.selector_chapter = selector_chapter  # 修正拼写错误
        self.max_retries = 1  # 最大重试次数
        self.retry_delay = 1  # 重试等待时间（秒）
        self.max_workers = max_workers

    def download_chapters(self):
        try:
            requester = RequestChapterURL(self.baseurl, self.url_path, self.selector_chapter)
            chapters = requester.get_chapter_links_and_titles()

            if not chapters:
                logging.error("未获取到任何章节链接！请检查选择器或网络连接")
                return

            async_downloader = AsyncChapterDownloader(max_workers=self.max_workers, max_retries=self.max_retries,
                                                      retry_delay=self.retry_delay)
            chapter_contents, failed_chapters = async_downloader.download_chapters(chapters, self.selector_content)

            self.save_to_file(chapter_contents)
            return len(failed_chapters)
        except Exception as e:
            logging.critical(f"致命错误: {str(e)}")
            return -1

    def save_to_file(self, chapter_contents):
        """增强文件保存错误处理"""
        try:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                for title, content in chapter_contents.items():
                    f.write(f"{title}\n{content}\n\n")
            logging.info(f"成功保存 {len(chapter_contents)} 章到 {self.output_file}")
        except IOError as e:
            logging.error(f"文件保存失败: {str(e)}")
            raise
        except Exception as e:
            logging.error(f"意外保存错误: {str(e)}")
            raise


if __name__ == '__main__':
    # 参数修正：selector_content 和 selector_chapter 的顺序
    downloader = NovelDownloader(
        baseurl="https://m.bqug8.com/",
        url_path='kan/131238/list.html',
        output_file='novel_unfinished.txt',
        selector_content='#chaptercontent',  # 内容选择器
        selector_chapter='.listmain a', # 章节选择器
        max_workers=30
    )

    result = downloader.download_chapters()
    if result == 0:
        print("所有章节下载完成！")
    elif result > 0:
        print(f"成功下载大部分内容，但有 {result} 章失败")
    else:
        print("下载过程遇到严重错误，请检查日志")
