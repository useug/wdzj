import scrapy
from wdzj.items import ExposureItem


class P2peyeSpider(scrapy.Spider):
    name = 'p2peye'
    allowed_domains = ['www.p2peye.com']
    base_url = "https://www.p2peye.com/forum-60-"
    index = 1
    html = ".html"
    start_urls = [
        base_url + str(index) + html
    ]
    sum = []
    # 配置爬虫使用的pipelines
    custom_settings = {
        'ITEM_PIPELINES': {
            'wdzj.pipelines.ExposurePipeline': 301
        }
    }

    def parse(self, response):
        items = ExposureItem()
        infos = response.xpath("//div[@class = 'ui-forumlist-item-wrap']")
        for info in infos:
            item = {}
            item['title'] = self.getTitle(info)
            item['url'] = self.getUrl(info)
            item['stick'] = self.getStick(info)
            self.sum.append(item)

        if self.index < 1:
            self.index += 1
            yield scrapy.Request(url=self.base_url + str(self.index) + self.html, callback=self.parse)
        else:
            items["datas"] = self.sum
            yield items

    def getTitle(self, data):
        title = data.xpath("./div[@class = 'ui-forumlist-title']/a/text()")
        if len(title) != 0:
            return title.extract()[0]
        else:
            return ""

    def getUrl(self, data):
        url = data.xpath("./div[@class = 'ui-forumlist-title']/a/@href")
        if len(url) != 0:
            return "https://www.p2peye.com/" + url.extract()[0]
        else:
            return ""

    def getStick(self, data):
        data = data.xpath("./div[@class = 'ui-forumlist-title']/span[1]/text()")
        if len(data) != 0:
            stick = data.extract()[0]
            if stick == '置顶':
                return '1'
            else:
                return '0'
        else:
            return '0'
