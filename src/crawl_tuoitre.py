import scrapy
import re
from pprint import pprint


class BrickSetSpider(scrapy.Spider):
    name = "article"
    domain = "https://news.ycombinator.com/news"
    start_urls = ['https://news.ycombinator.com/news']

    def parse(self, response):
        f = open("data/article.txt", "a")
        SET_SELECTOR = 'table .itemlist'
        body_mid = response.css(SET_SELECTOR)
        data_title = body_mid.css('tr.athing')
        data_info = body_mid.css('tr td.subtext')
        for i, data in enumerate(data_title):
            title = data.css('td.title a.storylink::text').get()
            author = data_info[i].css('a.hnuser::text').get()
            d = "{}, {}".format(title, author)
            f.write(d + "\n")
        import time
        time.sleep(3)
        f.close()
        NEXT_PAGE = "a.morelink::attr(href)"
        body = response.css(NEXT_PAGE).extract_first()
        print(response.css(NEXT_PAGE))
        if body:
            yield scrapy.Request(
                response.urljoin(body),
                callback=self.parse
            )
