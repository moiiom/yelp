# -*-coding:utf-8-*-
import time
import random
from scrapy import log
from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware
from scrapy.contrib.downloadermiddleware.defaultheaders import DefaultHeadersMiddleware
from settings import USER_AGENT_LIST, FETCH_PROXY_INTERVAL
from fetch_free_proxyes import fetch_all
from constants import MyGlobals


class MyHeadersMiddleware(DefaultHeadersMiddleware):
    def process_request(self, request, spider):
        pass


class MyUserAgentMiddleware(UserAgentMiddleware):
    def __init__(self, user_agent=''):
        self.user_agent = user_agent

    def process_request(self, request, spider):
        ua = random.choice(USER_AGENT_LIST)
        if ua:
            log.msg('Current UserAgent: ' + ua, level=log.INFO)
            request.headers.setdefault('User-Agent', ua)


class MyHttpProxyMiddleware(object):
    def process_request(self, request, spider):
        curr_time = time.time()
        local_proxy = '127.0.0.1:80'

        if not MyGlobals.last_fetch_time or curr_time > MyGlobals.last_fetch_time + FETCH_PROXY_INTERVAL:
            log.msg('start fetch proxy ips...', level=log.INFO)
            MyGlobals.proxy_list = fetch_all()
            MyGlobals.proxy_list.append(local_proxy)
            MyGlobals.last_fetch_time = curr_time

        proxy = random.choice(MyGlobals.proxy_list)
        if local_proxy == proxy:
            log.msg('*******current proxy is:local', level=log.INFO)
        else:
            log.msg('*******current proxy is:{0}'.format(proxy))
            request.meta['proxy'] = "http://%s" % proxy
