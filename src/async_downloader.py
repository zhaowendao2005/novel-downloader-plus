# async_downloader.py
import concurrent.futures
import logging
import time
from chapter_downloader import ChapterDownloader


class AsyncChapterDownloader:
    def __init__(self, max_workers=5, max_retries=1, retry_delay=1):
        self.max_workers = max_workers
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def _download_single_chapter(self, chapter, selector_content, index):
        chapter_url = chapter['url']
        title = chapter['title']
        logging.info(f"正在下载 ({title}) asynchronously")
        for attempt in range(self.max_retries):
            try:
                downloader = ChapterDownloader(chapter_url, selector_content)
                content = downloader.get_chapter_content()
                if not content.strip():
                    raise ValueError("获取到空内容")
                logging.info(f"成功下载: {title}")
                return index, title, content, None
            except Exception as e:
                logging.warning(f"第{attempt + 1}次尝试失败 ({title}): {str(e)}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
        logging.error(f"章节下载失败: {title}")
        return index, title, None, "Failed"

    def download_chapters(self, chapters, selector_content):
        chapter_contents = {}
        failed_chapters = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_chapter = {
                executor.submit(self._download_single_chapter, chapter, selector_content, index): index
                for index, chapter in enumerate(chapters)
            }
            results = []
            for future in concurrent.futures.as_completed(future_to_chapter):
                results.append(future.result())

        results.sort(key=lambda x: x[0])  # Sort by index
        for index, title, content, error in results:
            if error:
                failed_chapters.append(title)
            else:
                chapter_contents[title] = content

        if failed_chapters:
            logging.error("以下章节未能成功下载:\n" + "\n".join(failed_chapters))
        return chapter_contents, failed_chapters