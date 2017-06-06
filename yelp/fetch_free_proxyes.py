#!/usr/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import logging
import math
import threading

logger = logging.getLogger(__name__)


def get_html(url):
    request = urllib2.Request(url)
    request.add_header("User-Agent",
                       "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.99 Safari/537.36")
    html = urllib2.urlopen(request)
    return html.read()


def get_soup(url):
    soup = BeautifulSoup(get_html(url), "lxml")
    return soup


def fetch_kuaidaili():
    """
    从http://www.kuaidaili.com/抓取免费代理
    """
    pages = 5
    proxyes, target_urls = [], []
    urls = [
        "http://www.kuaidaili.com/free/inha/{0:d}/",
        "http://www.kuaidaili.com/free/intr/{0:d}/",
        "http://www.kuaidaili.com/free/outha/{0:d}/",
        "http://www.kuaidaili.com/free/outtr/{0:d}/"
    ]
    for page in range(1, pages + 1):
        for url in urls:
            target_urls.append(url.format(page))

    logger.info("fetch proxy ip from kuaidaili...")
    try:
        for url in target_urls:
            soup = get_soup(url)
            table = soup.find("table")
            trs = table.find_all("tr")
            for i in range(1, len(trs)):
                tr = trs[i]
                tds = tr.find_all("td")
                ip = tds[0].text
                port = tds[1].text
                # speed = tds[6].div["title"][:-1]
                # latency = tds[7].div["title"][:-1]
                # if float(speed) < 3 and float(latency) < 1:
                proxyes.append("%s:%s" % (ip, port))
    except:
        logger.warning("fail to fetch from kuaidaili")
    return proxyes


def fetch_kxdaili():
    """
    从www.kxdaili.com抓取免费代理
    """
    logger.info("fetch proxy ip from kxdaili...")
    proxyes = []
    for page in range(1, 11):
        try:
            url = "http://www.kxdaili.com/ipList/{0:d}.html#ip".format(page)
            soup = get_soup(url)
            table_tag = soup.find("table", attrs={"class": "ui table segment"})
            trs = table_tag.tbody.find_all("tr")
            for tr in trs:
                tds = tr.find_all("td")
                ip = tds[0].text
                port = tds[1].text
                latency = tds[4].text.split(" ")[0]
                if float(latency) < 5:  # 输出延迟小于5秒的代理
                    proxy = "%s:%s" % (ip, port)
                    proxyes.append(proxy)
        except:
            logger.warning("fail to fetch from kxdaili")
    return proxyes


def img2port(img_url):
    """
    mimvp.com的端口号用图片来显示, 本函数将图片url转为端口, 目前的临时性方法并不准确
    """
    code = img_url.split("=")[-1]
    if code.find("AO0OO0O") > 0:
        return 80
    else:
        return None


def fetch_mimvp():
    """
    从http://proxy.mimvp.com/free.php抓免费代理
    """
    proxyes = []
    try:
        url = "http://proxy.mimvp.com/free.php?proxy=in_hp"
        soup = get_soup(url)
        table = soup.find("div", attrs={"id": "list"}).table
        tds = table.tbody.find_all("td")
        for i in range(0, len(tds), 10):
            id = tds[i].text
            ip = tds[i + 1].text
            port = img2port(tds[i + 2].img["src"])
            response_time = tds[i + 7]["title"][:-1]
            transport_time = tds[i + 8]["title"][:-1]
            if port is not None and float(response_time) < 1:
                proxy = "%s:%s" % (ip, port)
                proxyes.append(proxy)
    except:
        logger.warning("fail to fetch from mimvp")
    return proxyes


def fetch_xici():
    """
    http://www.xicidaili.com/nn/
    """
    logger.info("fetch proxy ip from xici...")
    pages = 5
    proxyes, target_urls = [], []
    urls = [
        "http://www.xicidaili.com/nn/{0:d}",
        "http://www.xicidaili.com/wn/{0:d}",
        "http://www.xicidaili.com/wt/{0:d}"
    ]
    for page in range(1, pages + 1):
        for url in urls:
            target_urls.append(url.format(page))

    try:
        for url in target_urls:
            soup = get_soup(url)
            table = soup.find("table", attrs={"id": "ip_list"})
            trs = table.find_all("tr")
            for i in range(1, len(trs)):
                tr = trs[i]
                tds = tr.find_all("td")
                ip = tds[1].text
                port = tds[2].text
                speed = tds[6].div["title"][:-1]
                latency = tds[7].div["title"][:-1]
                if float(speed) < 3 and float(latency) < 1:
                    proxyes.append("%s:%s" % (ip, port))
    except:
        logger.warning("fail to fetch from xici")
    return proxyes


def fetch_ip181():
    """
    http://www.ip181.com/
    """
    logger.info("fetch proxy ip from ip181...")
    proxyes = []
    try:
        url = "http://www.ip181.com/"
        soup = get_soup(url)
        table = soup.find("table")
        trs = table.find_all("tr")
        for i in range(1, len(trs)):
            tds = trs[i].find_all("td")
            ip = tds[0].text
            port = tds[1].text
            latency = tds[4].text[:-2]
            if float(latency) < 1:
                proxyes.append("%s:%s" % (ip, port))
    except Exception as e:
        logger.warning("fail to fetch from ip181: %s" % e)
    return proxyes


def fetch_httpdaili():
    """
    http://www.httpdaili.com/mfdl/
    更新比较频繁
    """
    logger.info("fetch proxy ip from httpdaili...")
    proxyes = []
    try:
        url = "http://www.httpdaili.com/mfdl/"
        soup = get_soup(url)
        trs = soup.find_all("tr")
        for tr in trs:
            try:
                tds = tr.find_all("td")[1:]
                ip = tds[0].text
                port = tds[1].text
                type = tds[2].text
                # if type == u"匿名":
                proxyes.append("%s:%s" % (ip, port))
            except:
                pass
    except Exception as e:
        logger.warning("fail to fetch from httpdaili: %s" % e)
    return proxyes


def fetch_66ip():
    """
    http://www.66ip.cn/
    每次打开此链接都能得到一批代理, 速度不保证
    """
    logger.info("fetch proxy ip from 66ip...")
    proxyes = []
    pages = 5
    proxyes, target_urls = [], []
    urls = [
        "http://www.66ip.cn/areaindex_33/{0:d}.html",
        "http://www.66ip.cn/areaindex_34/{0:d}.html"
    ]
    for page in range(1, pages + 1):
        for url in urls:
            target_urls.append(url.format(page))

    try:
        for url in target_urls:
            soup = get_soup(url)
            table = soup.find("div", attrs={"id": "footer"})
            trs = table.find_all("tr")[1:]
            for i in range(1, len(trs)):
                tr = trs[i]
                tds = tr.find_all("td")
                ip = tds[0].text
                port = tds[1].text
                proxyes.append("%s:%s" % (ip, port))
    except:
        logger.warning("fail to fetch from xici")
    return proxyes


def fetch_us_proxy():
    """
    https://www.us-proxy.org/
    每次打开此链接都能得到一批代理, 速度不保证
    """
    logger.info("fetch proxy ip from us proxy...")
    proxyes = []
    urls = [
        "https://free-proxy-list.net",
        "https://www.sslproxies.org",
        "https://www.us-proxy.org",
    ]

    try:
        for url in urls:
            soup = get_soup(url)
            table = soup.find("table")
            trs = table.find_all("tr")
            for i in range(1, len(trs)):
                tr = trs[i]
                tds = tr.find_all("td")
                ip = tds[0].text
                port = tds[1].text
                proxyes.append("%s:%s" % (ip, port))
    except:
        logger.warning("fail to fetch from us proxy")
    return proxyes


def fetch_my_proxy():
    """
    https://www.my-proxy.com
    每次打开此链接都能得到一批代理, 速度不保证
    """
    logger.info("fetch proxy ip from my proxy...")
    proxyes = []
    pages = 10
    proxyes, target_urls = [], []
    urls = [
        "https://www.my-proxy.com/free-proxy-list-{0:d}.html",
    ]
    for page in range(1, pages + 1):
        for url in urls:
            target_urls.append(url.format(page))

    try:
        for url in target_urls:
            soup = get_soup(url)
            table = soup.find("div", attrs={"id": "footer"})
            trs = table.find_all("tr")[1:]
            for i in range(1, len(trs)):
                tr = trs[i]
                tds = tr.find_all("td")
                ip = tds[0].text
                port = tds[1].text
                proxyes.append("%s:%s" % (ip, port))
    except:
        logger.warning("fail to fetch from my proxy")
    return proxyes


def check(unverify, verify):
    num, total = 1, len(unverify)
    for proxy in unverify:
        import urllib2
        url = "https://www.yelp.com"
        proxy_handler = urllib2.ProxyHandler({'https': "http://" + proxy})
        opener = urllib2.build_opener(proxy_handler, urllib2.HTTPHandler)
        try:
            response = opener.open(url, timeout=3)
            logger.info("+++Check Success({0:d}/{1:d}):{2}".format(num, total, proxy))
            verify.append(proxy)
        except Exception:
            logger.info("---Check Failure({0:d}/{1:d}):{0}".format(num, total, proxy))
        finally:
            num += 1


def fetch_all():
    data_size = 50
    proxyes, valid_proxyes, double_valid_proxyes = list(), list(), list()
    proxyes += fetch_kuaidaili()
    proxyes += fetch_kxdaili()
    proxyes += fetch_xici()
    proxyes += fetch_ip181()
    proxyes += fetch_66ip()

    # proxyes += fetch_mimvp()
    # proxyes += fetch_httpdaili()

    proxyes += fetch_us_proxy()
    # proxyes += fetch_my_proxy()

    logger.info("checking proxyes validation,total:{0:d}".format(len(proxyes)))
    # *************************multi thread check***************************
    all_thread = []
    num = int(math.ceil(len(proxyes) / float(data_size)))
    for i in range(num):
        start = data_size * i
        end = data_size * (i + 1)
        t = threading.Thread(target=check, args=(proxyes[start:end], valid_proxyes))
        all_thread.append(t)
        t.start()
    for t in all_thread:
        t.join()
    # ***********************************************************************
    # check(proxyes, valid_proxyes)
    check(list(set(valid_proxyes)), double_valid_proxyes)
    return double_valid_proxyes


if __name__ == '__main__':
    import sys

    root_logger = logging.getLogger("")
    stream_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(name)-8s %(asctime)s %(levelname)-8s %(message)s', '%a, %d %b %Y %H:%M:%S', )
    stream_handler.setFormatter(formatter)
    root_logger.addHandler(stream_handler)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    proxyes = fetch_all()
    # print check("202.29.238.242:3128")
    for p in proxyes:
        print p
