import scrapy
from wdzj.items import WdzjHotItem


class WdzjhotSpider(scrapy.Spider):
    # 爬虫名
    name = 'wdzjhot'
    # 允许的域名
    allowed_domains = ['www.p2peye.com']
    # 入口的url，扔到调度器里面,这里是地址前缀
    base_url = 'http://www.p2peye.com/forumlist-10-'
    # 第一页
    index = 1
    # 后缀
    html = ".html"
    # 入口的url，扔到调度器里面
    start_urls = [base_url + str(index) + html]

    sum = []

    # 配置爬虫使用的pipelines
    custom_settings = {
        'ITEM_PIPELINES': {
            'wdzj.pipelines.WdzjHotPipeline': 302
        }
    }

    def parse(self, response):
        hot_item = WdzjHotItem()
        hot_list = response.xpath("//div[@class='ui-tabskin']//ul[@class='ui-tabskin-body ui-forumlist']/li")

        for i_item in hot_list:
            hot_items = {}
            # 标题
            hot_items['title'] = i_item.xpath(
                ".//div[@class='ui-forumlist-item-main']//div[@class='ui-forumlist-title']/a/text()").extract_first()
            # 来源
            hot_items['source'] = i_item.xpath(
                ".//div[@class='ui-forumlist-item-main']//div[@class='ui-forumlist-info']/a/text()").extract_first()
            # 时间
            hot_items['exposure_time'] = i_item.xpath(
                ".//div[@class='ui-forumlist-item-main']//div[@class='ui-forumlist-info']/span[2]/text()").extract_first()
            # 链接
            hot_items['url'] = "https://www.p2peye.com" + i_item.xpath(
                ".//div[@class='ui-forumlist-item-main']//div[@class='ui-forumlist-title']/a/@href").extract_first()
            self.sum.append(hot_items)
            # yield hot_item

            if self.index < 1:
                self.index += 1
                yield scrapy.Request(url=self.base_url + str(self.index) + self.html, callback=self.parse)
            else:
                hot_item["datas"] = self.sum
                yield hot_item
