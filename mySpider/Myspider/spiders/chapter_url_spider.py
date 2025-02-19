import scrapy

class ChapterUrlSpiderSpider(scrapy.Spider):
    name = "chapter_url_spider"
    allowed_domains = ["m.bqug8.com"]
    start_urls = ["https://m.bqug8.com/kan/37264/list.html"]

    class ChapterItem(scrapy.Item):
        chapter = scrapy.Field()
        url = scrapy.Field()

    def parse(self, response):
        for each in response.css("div.listmain"):
            item = self.ChapterItem()
            chapter = each.css("dd a::text").getall()
            url = each.css("dd a::attr(href)").getall()
            item['chapter'] = chapter
            item['url'] = url

            yield item  # Yield the item instead of printing it