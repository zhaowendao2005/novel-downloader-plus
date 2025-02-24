import requests
from bs4 import BeautifulSoup
import logging
import traceback
import time

from twisted.web.html import output

from .request_chatper_url import RequestChapterURL

from .async_downloader import AsyncChapterDownloader

# 配置日志系统
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('../../../novel_downloader.log'),
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
        self.interrupt_check = None

    def set_interrupt_check(self, callback):
        """设置中断检查回调方法"""
        self.interrupt_check = callback




    def download_chapters(self):
        try:
            requester = RequestChapterURL(self.baseurl, self.url_path, self.selector_chapter)
            chapters = requester.get_chapter_links_and_titles()

            # 新增中断检查点
            if self.interrupt_check and self.interrupt_check():
                logging.warning("下载被用户中断")
                return -2  # 用特定代码表示用户中断

            async_downloader = AsyncChapterDownloader(
                max_workers=self.max_workers,
                max_retries=self.max_retries,
                retry_delay=self.retry_delay
            )

            # 传递中断检查给async_downloader
            chapter_contents, failed_chapters = async_downloader.download_chapters(
                chapters,
                self.selector_content,
                self.interrupt_check  # 传递中断检查回调
            )

            # 定期检查中断
            for i, (title, content) in enumerate(chapter_contents.items()):
                if i % 10 == 0 and self.interrupt_check and self.interrupt_check():
                    logging.warning("保存过程中检测到中断请求")
                    return -2

            self.save_to_file(chapter_contents)
            return len(failed_chapters)
        except KeyboardInterrupt:
            logging.warning("捕获到键盘中断信号")
            return -2
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
