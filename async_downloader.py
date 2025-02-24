
# async_downloader.py
import concurrent.futures  # 新增的导入
import logging
import time
from chapter_downloader import ChapterDownloader





class AsyncChapterDownloader:
    def __init__(self, max_workers=5, max_retries=1, retry_delay=1):
        self.max_workers = max_workers
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def download_chapters(self, chapters, selector_content, interrupt_check=None):
        """
        新增参数说明：
        :param interrupt_check: 可调用对象，返回bool表示是否需要中断
        """
        chapter_contents = {}
        failed_chapters = []

        with concurrent.futures.ThreadPoolExecutor(
                max_workers=self.max_workers,
                thread_name_prefix="DownloadWorker"  # 方便调试
        ) as executor:
            # 1. 任务提交阶段
            future_to_index = {
                executor.submit(
                    self._download_single_chapter,
                    chapter,
                    selector_content,
                    index,
                    interrupt_check  # 传递中断检查到每个任务
                ): index
                for index, chapter in enumerate(chapters)
            }

            try:
                # 2. 结果收集阶段
                for future in concurrent.futures.as_completed(future_to_index):
                    # 关键中断检查点
                    if interrupt_check and interrupt_check():
                        logging.warning("检测到中断信号，终止下载...")

                        # 立即关闭线程池
                        executor.shutdown(wait=False, cancel_futures=True)

                        # 清空未完成结果
                        chapter_contents.clear()
                        failed_chapters.append("用户中断下载")
                        return chapter_contents, failed_chapters

                    # 正常处理结果
                    index, title, content, error = future.result()
                    if error:
                        failed_chapters.append(title)
                    else:
                        chapter_contents[title] = content

            except concurrent.futures.CancelledError:
                logging.warning("任务被用户取消")
                return chapter_contents, failed_chapters

        # 3. 结果排序处理（保持原有逻辑）
        sorted_results = sorted(
            (future.result() for future in future_to_index if future.done()),
            key=lambda x: x[0]
        )

        # ...后续处理逻辑保持不变...
        return chapter_contents, failed_chapters

    def _download_single_chapter(self, chapter, selector_content, index, interrupt_check=None):
        """单章节下载方法"""
        for attempt in range(self.max_retries):
            # 每次重试前检查中断
            if interrupt_check and interrupt_check():
                logging.info(f"中断请求，放弃下载: {chapter['title']}")
                return index, chapter['title'], None, "用户中断"

            try:
                # 原有下载逻辑...
                downloader = ChapterDownloader(...)
                content = downloader.get_chapter_content()
                # ...
            except Exception as e:
                # 在异常处理中添加中断检查
                if interrupt_check and interrupt_check():
                    logging.info(f"中断请求，放弃重试: {chapter['title']}")
                    break
                # ...原有重试逻辑...

        # ...最终返回结果...
