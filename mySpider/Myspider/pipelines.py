# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class MyspiderPipeline:

    def process_item(self, item, spider):
        #将item中的数据写入文件
        with open("chapter_url.txt", "a", encoding="utf-8") as f:
            f.write(str(item) + "\n")
        return item