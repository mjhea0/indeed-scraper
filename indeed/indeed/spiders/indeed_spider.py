from scrapy import Spider
from scrapy.selector import HtmlXPathSelector

from indeed.items import IndeedItem


class IndeedSpider(Spider):
    name = "indeed"
    allowed_domains = ["indeed.com"]
    start_urls = [
        "http://www.indeed.com/jobs?q=veterinarian&l=Denver&limit=50",
    ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        sites = hxs.xpath('//div[@class="row  result"]')
        items = []
        for site in sites:
            item = IndeedItem(company='none')

            item['job_title'] = site.xpath('h2/a/@title').extract()
            item['link_url'] = site.xpath('h2/a/@href').extract()

            # item['location'] = site.xpath(
            #     'span[@class="location"]/span/text()').extract()

            # Not all entries have a company
            if site.xpath("span[@class='company']/text()").extract() == []:
                item['company'] = [u'']
            else:
                item['company'] = site.xpath(
                    "span[@class='company']/text()").extract()

            item['summary'] = site.xpath(
                "//table/tr/td/span[@class='summary']").extract()
            item['source'] = site.xpath(
                "table/tr/td/span[@class='source']/text()").extract()
            item['found_date'] = site.xpath(
                "table/tr/td/span[@class='date']/text()").extract()
            items.append(item)
        print items
