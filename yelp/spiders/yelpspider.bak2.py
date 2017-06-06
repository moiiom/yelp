#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import re
import sys
import errno
import codecs
import scrapy
import urlparse

from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import Selector
from yelp.items import YelpItem
from yelp.constants import MyGlobals

reload(sys)
sys.setdefaultencoding('utf-8')


class YelpSpider(CrawlSpider):
    pagesize = 10
    name = "yelpspider"
    allowed_domains = ["www.yelp.com"]

    def __init__(self, *args, **kwargs):
        super(YelpSpider, self).__init__(*args, **kwargs)

        self.allowed_domains = ["www.yelp.com"]
        self.start_urls = self._get_start_urls()

    def parse(self, response):
        print response.url
        exts = response.xpath('//div[@class="page-of-pages arrange_unit arrange_unit--fill"]/text()').extract()
        if len(exts) < 1:
            return

        total = int(exts[0].replace('\n', '').strip().split(" ")[3])
        links = self._get_page_links(total, response.url)
        for _ in links:
            yield scrapy.Request(_, callback=self.detail_parse)

    def detail_parse(self, response):
        print response.url
        city = self._get_city_from_url(response.url)
        filename = "data/{0}/{1}.csv".format(self.allowed_domains[0], city)
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise

        contexts = response.xpath('//li[@class="regular-search-result"]/div').extract()
        for c in contexts:
            s = Selector(text=c)
            item = YelpItem()
            item['name'] = [_.replace('\n', '').replace('\t', '').strip() for _ in
                            s.xpath('//a[@class="biz-name js-analytics-click"]//text()').extract()]
            item['address'] = [_.replace('\n', '').replace('\t', '').strip() for _ in
                               s.xpath('//address/text()').extract()]
            item['phone'] = [_.replace('\n', '').replace('\t', '').strip() for _ in
                             s.xpath('///span[@class="biz-phone"]/text()').extract()]
            item['categories.csv'] = [_.replace('\n', '').replace('\t', '').strip() for _ in
                                  s.xpath('//span[@class="category-str-list"]/a/text()').extract()]
            item['img'] = s.xpath('//div[@class="photo-box pb-90s"]/a/img/@src').extract()[0]

            with codecs.open(filename, 'a', 'utf-8') as f:
                f.write(
                    "{0}\t{1}\t{2}\t{3}\t{4}\n".format(','.join(item['name']), ','.join(item['address']),
                                                  ','.join(item['phone']),
                                                  ','.join(item['categories.csv']),
                                                           item['img']))
            yield item

    @staticmethod
    def _get_city_from_url(url):
        query = urlparse.urlparse(url).query
        parm = dict([(k, v[0]) for k, v in urlparse.parse_qs(query).items()])
        return parm.get('find_loc')

    @staticmethod
    def _get_start_urls():
        urls = list()
        for city in MyGlobals.city_list:
            for busi in MyGlobals.busi_list:
                url = "http://www.yelp.com/search?find_loc={0}&categories.csv={1}".format(city, busi)
                urls.append(url)
        return urls

    def _preprocess(self, parameter):
        match = re.compile(r'\w+').findall(parameter)
        if match:
            return match
        else:
            return []

    def _get_page_links(self, total, url):
        links = []
        for i in range(1, total):
            if i == 1:
                links.append(url)
            else:
                links.append(url + "&start=" + str((i - 1) * self.pagesize))
        return links
