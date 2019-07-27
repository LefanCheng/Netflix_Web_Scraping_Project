from scrapy import Spider, Request
from imbd.items import ImbdItem
import re

class ImbdSpider(Spider):
    name = 'imbd_spider'
    allowed_urls = ['https://www.imdb.com/']
    start_urls = ['https://www.imdb.com/search/title/?companies=co0144901']

    def parse(self, response):
        result_urls = ['https://www.imdb.com/search/title/?companies=co0144901&start={}&ref_=adv_nxt'.format(x) for x in range(51,6000,50)]
        for url in result_urls:
            yield Request(url=url, callback=self.parse_result_page)

    def parse_result_page(self, response):
        detail_urls = response.xpath('//*[@id="main"]/div//h3[@class="lister-item-header"]/a/@href').extract()

        for url in detail_urls:
            yield Request(url='https://www.imdb.com/' + url, callback=self.parse_detail_page)

    def parse_detail_page(self, response):
        title = response.xpath('//div[@class="title_wrapper"]/h1/text()').extract_first().strip()
        avg_rating = response.xpath('//span[@itemprop="ratingValue"]/text()').extract_first()
        rating_count = response.xpath('//span[@itemprop="ratingCount"]/text()').extract_first()
        num_reviews = re.findall( '\d+',response.xpath('//div[@class="user-comments"]//a/text()').extract()[3])[0]

        item = ImbdItem()
        item['title'] = title
        item['avg_rating'] = avg_rating
        item['rating_count'] = rating_count
        item['num_reviews'] = num_reviews

        yield item