import scrapy
from wdzj.items import WdzjItem
from lxml import etree


class WdzjNewsSpider(scrapy.Spider):
    name = 'wdzj_news'
    allowed_domains = ['bbs.wdzj.com']
    start_urls = ['http://bbs.wdzj.com/forum-110-1.html?orderby=create_time/']

    base_url = "http://bbs.wdzj.com/forum-110-"
    index = 1
    html = ".html?orderby=create_time/"
    start_urls = [
        base_url + str(index) + html
    ]
    sum = []

    custom_settings = {
        'ITEM_PIPELINES': {
            'wdzj.pipelines.WdzjPipeline': 300
        }
    }

    # 对请求返回的网页HTML代码进行处理

    def parse(self, response):
        items = WdzjItem()
        selector = etree.HTML(response.text)
        htmls = selector.xpath("//div[@class = 'detail-ul-txt detail-ulcur']/ul/li")
        for html in htmls:
            item = {}
            item['title'] = html.xpath("normalize-space(./div[@class = 'theme-txt fleft']/a/h3/span/text())")
            item['source'] = html.xpath("./div[@class = 'theme-txt fleft']/div/div[@class = 'theme-lf fleft']/a/text()")
            item['exposure_time'] = html.xpath(
                "./div[@class = 'theme-txt fleft']/div/div[@class = 'theme-lf fleft']/span/a/text()")
            item['url'] = html.xpath("./div[@class = 'theme-txt fleft']/a/@href")
            alt = html.xpath("./div[@class = 'theme-txt fleft']/a/h3/img/@alt")
            if len(alt):  # 存在为置顶
                item['is_top'] = 1
            else:
                item['is_top'] = 0

            self.sum.append(item)

        if self.index < 1:
            self.index += 1
            yield scrapy.Request(url=self.base_url + str(self.index) + self.html, callback=self.parse)
        else:
            items["datas"] = self.sum
            yield items
