import scrapy
import re
from pprint import pprint


class BrickSetSpider(scrapy.Spider):
    name = "article"
    domain = "https://diemthi.vnexpress.net"
    start_urls = ['https://diemthi.vnexpress.net']

    def parse(self, response):
        f = open("data/scores.txt", "a")
        SET_SELECTOR = 'body'
        body_mid = response.css(SET_SELECTOR)
        print(body_mid)
        print("len =", len(body_mid))
        print("len1 =", len(body_mid.css('svg')))
        return
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
