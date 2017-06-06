#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import scrapy
import urlparse
import datetime

from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import Selector
from yelp.items import YelpItem
from yelp.constants import MyGlobals
from yelp.settings import DATA_BASE_PATH

reload(sys)
sys.setdefaultencoding('utf-8')


class YelpSpider(CrawlSpider):
    pagesize = 10
    name = "yelpspider"
    allowed_domains = ["www.yelp.com"]
    base_url = "http://www.yelp.com"
    data_date = datetime.datetime.now().strftime('%Y%m%d')

    def __init__(self, *args, **kwargs):
        super(YelpSpider, self).__init__(*args, **kwargs)
        # self.start_urls = self._get_start_urls()
        self.start_urls = ["http://www.yelp.com/search?find_loc=Aberdeen%2C+WA&cflt=financialservices"]

    def parse(self, response):
        print response.url

        exts = response.xpath('//div[@class="page-of-pages arrange_unit arrange_unit--fill"]/text()').extract()
        if len(exts) < 1:
            return

        total = int(exts[0].replace('\n', '').strip().split(" ")[3])
        links = self._get_page_links(total, response.url)
        for _ in links:
            # yield scrapy.Request(_, headers=headers, callback=self.detail_parse)
            yield scrapy.Request(_, callback=self.detail_parse)

    def detail_parse(self, response):
        print response.url
        city = self._get_city_from_url(response.url)
        filename = "{0}/{1}/{2}/{3}.csv".format(DATA_BASE_PATH, self.data_date, self.allowed_domains[0], city)

        contexts = response.xpath('//li[@class="regular-search-result"]/div').extract()
        for c in contexts:
            s = Selector(text=c)
            item = YelpItem()
            item['filename'] = filename
            item['name'] = [_.replace('\n', '').replace('\t', '').strip() for _ in
                            s.xpath('//a[@class="biz-name js-analytics-click"]//text()').extract()]
            item['address'] = [_.replace('\n', '').replace('\t', '').strip() for _ in
                               s.xpath('//address/text()').extract()]
            item['phone'] = [_.replace('\n', '').replace('\t', '').strip() for _ in
                             s.xpath('///span[@class="biz-phone"]/text()').extract()]
            item['categories'] = [_.replace('\n', '').replace('\t', '').strip() for _ in
                                      s.xpath('//span[@class="category-str-list"]/a/text()').extract()]
            item['img'] = s.xpath('//div[@class="photo-box pb-90s"]/a/img/@src').extract()[0]
            yield item

    @staticmethod
    def _get_city_from_url(url):
        url = url.replace('%2C+', '').replace('+', '')
        query = urlparse.urlparse(url).query
        parm = dict([(k, v[0]) for k, v in urlparse.parse_qs(query).items()])
        return parm.get('find_loc')

    def _get_start_urls(self):
        urls = list()
        for (state, cities) in MyGlobals.americian_cities.items():
            for city in cities:
                loc = city.replace(' ', '+') + "%2C+" + state
                for (top, sec) in MyGlobals.find_cflt.items():
                    if sec:
                        for cflt in sec:
                            urls.append("{0}/search?find_loc={1}&cflt={2}".format(self.base_url, loc, cflt))
                    else:
                        urls.append("{0}/search?find_loc={1}&cflt={2}".format(self.base_url, loc, top))
        return urls

    def _get_page_links(self, total, url):
        links = [url]
        for i in range(1, total+1):
            if i > 1:
                links.append(url + "&start=" + str((i - 1) * self.pagesize))
        return links