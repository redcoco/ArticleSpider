# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from fake_useragent import UserAgent
import json

class ArticlespiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RandomUserAgentMiddleware(object):
    #随机切换user-agent
    def __init__(self,crawler):
        super(RandomUserAgentMiddleware).__init__()
        # self.user_agent_list = crawler.settings.get("user_agent_list")
        self.ua = UserAgent()
        self.ua_type = crawler.settings.get("RANDOM_UA_TYPE","random")
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        # import random
        # request.headers.setdefault(b'User-Agent', random(self.user_agent_list))
        def get_ua():
            return getattr(self.ua,self.ua_type) # 等同 ua.ua_type ua.random
        random_ua =  get_ua()
        request.headers.setdefault(b'User-Agent', get_ua())
class RandomHttpProxyMiddleware(object):
    def get_random_proxy(self):
        with open('E:/downloads/ArticleSpider/tools/ips.txt', encoding="utf-8") as json_file:
            ip_lists = json.load(json_file)
        import random
        ip_index = random.randint(0,len(ip_lists)-1)
        ip_port = ip_lists[ip_index]
        proxy = "{0}://{1}:{2}".format(ip_port[2].lower(),ip_port[0],ip_port[1])
        return proxy


    def process_request(self, request, spider):
        request.meta["proxy"] = self.get_random_proxy()



from selenium import webdriver
from scrapy.http import HtmlResponse
class JSPageMiddleware(object):
    # 集成selenium通过chrome请求动态网页
    #  def __init__(self):
    #      self.browser = webdriver.Chrome(executable_path="C:/Users/wenjuan/PycharmProjects/chromedriver.exe")
    #      super(JSPageMiddleware,self).__init__()

    def process_request(self,request,spider):
        if spider.name == "jobbole":
            # self.browser.get(request.url)
            spider.browser.get(request.url)
            import time
            time.sleep(3)
            from scrapy.log import logger
            logger.info(msg="访问:{0}".format(request.url))
            print("访问:{0}".format(request.url))

            return HtmlResponse(url=spider.browser.current_url,body=spider.browser.page_source,request=request,encoding="utf-8")


# 无界面chrome
# from pyvirtualdisplay import Display
# display = Display(visible=0,size=(800,600)) # 0 不可见
# display.start()
# browser = webdriver.Chrome()
# browser.get()

