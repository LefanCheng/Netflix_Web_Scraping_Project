from scrapy import Spider, Request
from netflix_film.items import NetflixFilmItem
import re

class NetflixFilmSpider(Spider):
    name = 'netflix_film_spider'
    allowed_urls = ['https://en.wikipedia.org/']
    start_urls = ['https://en.wikipedia.org/wiki/List_of_original_films_distributed_by_Netflix']

    def parse(self, response):

        rows = response.xpath('//*[@id="mw-content-text"]/div/table/tbody/tr')

        for row in rows[1:]: 
            title = ""
            genre = ""
            premiere = ""
            length = ""
            language = ""
            status = ""
            distribution = ""

            title = row.xpath('./td[1]/i/a/text()').extract_first()
            genre = "/".join(row.xpath('./td/a[contains(@href, "/wiki/")]/text()').extract())
            premiere = row.xpath('./td/span[contains(@data-sort-value, "00000")]/text()').extract_first()              
            length = row.xpath('./td/span[contains(@data-sort-value, "!")]/text()').extract_first()
            language1 = './td[' + str(len(row.xpath('./td'))) + ']/text()'
            language = row.xpath(language1).extract_first()
            distribution = 'original film'
            
            item = NetflixFilmItem()
            item['title'] = title
            item['genre'] = genre
            item['premiere'] = premiere
            item['length'] = length
            item['language'] = language
            item['distribution'] = distribution
            yield item




