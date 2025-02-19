import requests
from bs4 import BeautifulSoup
import logging
import traceback
import time
from request_chatper_url import RequestChapterURL
from chapter_downloader import ChapterDownloader

# 配置日志系统
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('novel_downloader.log'),
        logging.StreamHandler()
    ]
)


class NovelDownloader:
    def __init__(self, baseurl, url_path, output_file, selector_content, selector_chapter):
        self.baseurl = baseurl
        self.url_path = url_path
        self.output_file = output_file
        self.selector_content = selector_content
        self.selector_chapter = selector_chapter  # 修正拼写错误
        self.max_retries = 3  # 最大重试次数
        self.retry_delay = 5  # 重试等待时间（秒）

    def download_chapters(self):
        """增强错误处理的章节下载方法"""
        try:
            requester = RequestChapterURL(self.baseurl, self.url_path, self.selector_chapter)
            chapters = requester.get_chapter_links_and_titles()

            if not chapters:
                logging.error("未获取到任何章节链接！请检查选择器或网络连接")
                return

            chapter_contents = {}
            failed_chapters = []

            for idx, chapter in enumerate(chapters, 1):
                chapter_url = chapter['url']
                chapter_title = chapter['title']
                logging.info(f"正在下载 ({idx}/{len(chapters)}) {chapter_title}")

                for attempt in range(self.max_retries):
                    try:
                        downloader = ChapterDownloader(chapter_url, self.selector_content)
                        content = downloader.get_chapter_content()

                        if not content.strip():
                            raise ValueError("获取到空内容")

                        chapter_contents[chapter_title] = content
                        break  # 成功则退出重试循环
                    except requests.exceptions.RequestException as e:
                        logging.warning(f"第{attempt + 1}次尝试失败 ({chapter_title}): 网络错误 - {str(e)}")
                    except (AttributeError, KeyError) as e:
                        logging.error(f"内容解析失败 ({chapter_title}): 选择器可能失效 - {str(e)}")
                        break  # 解析错误无需重试
                    except Exception as e:
                        logging.warning(f"第{attempt + 1}次尝试失败 ({chapter_title}): {str(e)}")

                    if attempt < self.max_retries - 1:
                        time.sleep(self.retry_delay)
                else:  # 所有重试均失败
                    failed_chapters.append(chapter_title)
                    logging.error(f"章节下载失败: {chapter_title}")
                    continue

                logging.info(f"成功下载: {chapter_title}")

            if failed_chapters:
                logging.error(f"以下章节未能成功下载:\n" + "\n".join(failed_chapters))

            self.save_to_file(chapter_contents)
            return len(failed_chapters)

        except Exception as e:
            logging.critical(f"致命错误: {str(e)}\n{traceback.format_exc()}")
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
        url_path='kan/37264/list.html',
        output_file='chapters_content.txt',
        selector_content='#chaptercontent',  # 内容选择器
        selector_chapter='.listmain a'  # 章节选择器
    )

    result = downloader.download_chapters()
    if result == 0:
        print("所有章节下载完成！")
    elif result > 0:
        print(f"成功下载大部分内容，但有 {result} 章失败")
    else:
        print("下载过程遇到严重错误，请检查日志")
