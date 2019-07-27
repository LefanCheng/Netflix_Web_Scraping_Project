from scrapy import Spider, Request
from netflix.items import NetflixItem
import re
import statistics

class NetflixSpider(Spider):
    name = 'netflix_spider'
    allowed_urls = ['https://en.wikipedia.org/']
    start_urls = ['https://en.wikipedia.org/wiki/List_of_original_programs_distributed_by_Netflix']

    def parse(self, response):
      
        rows = response.xpath('//*[@id="mw-content-text"]/div/table/tbody/tr')

        for row in rows:
            
            title = row.xpath('./td[1]/i/a/text()').extract_first()
            if not title:           
                title = row.xpath('./td[1]/a/i/text()').extract_first()
            if not title:
                title = row.xpath('./td[1]/span/i/a/text()').extract_first()
            if not title:
                title = row.xpath('./td[1]/i/text()').extract_first()

            genre = row.xpath('./td/a[contains(@href, "/wiki/")]/text()').extract_first()
            premiere = row.xpath('./td/span[contains(@data-sort-value, "00000")]/text()').extract_first()

            seasons2 = row.xpath('./td/span[contains(@data-sort-value, "!")]/text()').extract()
            seasons = "" 
            episodes = ""

            for i in seasons2:
                if re.search('min.', i) == None:
                    print(50*"*")
                    print(i)
                    if i.find(',') != -1:
                        episodes3 = ""
                        seasons3 = ""
                        seasons3, episodes3 = i.split(',')
                        episodes = int(re.search(r'(\d+)',episodes3).group())
                        seasons = int(re.search(r'(\d+)',seasons3).group())
                    else:
                        seasons = 1
                        episodes = int(re.search(r'(\d+)', i).group())
                    print(50*"*")
                else:
                    pass

            length2 = row.xpath('./td/span[contains(@data-sort-value, "!")]/text()').extract()
            length = ""

            for i in length2:
                if re.search('min.', i) == None:
                    pass
                else:
                    # length = statistics.mean([int(x) for x in re.search(r'(\d+–\d+)', i).group(0).split('–')])
                    length = i

            path = './td[' + str(len(row.xpath('./td'))) + ']/text()'
            status = row.xpath(path).extract_first()

            language = 'English'
            if re.search('Icelandic|Italian|Dutch|Hebrew|Thai|Irish|Chinese|Catalan|German|Korean|Filipino|English|Bulgarian|Russian|Mandarin|Swedish|Japanese|Polish|Turkish|Norwegian|Spanish|Danish|Portuguese|Arabic|Finnish|French|Galician', str(status)) != None:
                language = status

            if seasons == 1:
                item = NetflixItem()
                item['title'] = title
                item['genre'] = genre
                item['premiere'] = premiere
                item['seasons'] = seasons
                item['episodes'] = episodes
                item['length'] = length
                item['status'] = status
                item['language'] = language
                yield item
            else:
                title_urls = row.xpath('./td[1]/i/a/@href').extract()
                title_urls = ['https://en.wikipedia.org/' + s for s in title_urls]
                for url in title_urls:
                    yield Request(url=url, meta={'title':title,'genre':genre,'premiere':premiere,'seasons':seasons,'episodes':episodes,'length':length,'status':status,'language':language}, callback=self.parse_title_page)

    def parse_title_page(self, response):
        
        title = response.meta['title']
        genre = response.meta['genre']
        premiere = response.meta['premiere']
        seasons = response.meta['seasons']
        episodes = response.meta['episodes']
        length = response.meta['length']
        status = response.meta['status'] 
        language = response.meta['language']

        table_rows = response.xpath('//*[@id="mw-content-text"]/div/table[@class="wikitable plainrowheaders"][@style="text-align:center"][1]/tbody/tr')
        if table_rows:
            for table_row in table_rows:
                season = ""
                episode = ""
                released_date = ""
                season = table_row.xpath('./th[@scope="row"]/a/text()').extract()
                episode = table_row.xpath('./td[@colspan="2"]/text()').extract()
                released_date = table_row.xpath('./td[@colspan="1"]/span/span/text()').extract()
                
                item = NetflixItem()
                item['title'] = title
                item['genre'] = genre
                item['premiere'] = released_date
                item['seasons'] = season
                item['episodes'] = episode
                item['length'] = length
                item['status'] = status
                item['language'] = language

                yield item
        if not table_rows:
            for season in list(range(seasons)):
                item = NetflixItem()
                item['title'] = title
                item['genre'] = genre
                item['premiere'] = premiere
                item['seasons'] = seasons
                item['episodes'] = episodes
                item['length'] = length
                item['status'] = status
                item['language'] = language
                yield item