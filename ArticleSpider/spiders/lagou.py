# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ArticleSpider.items import LagouJobItem,LagouItemLoader
from ArticleSpider.utils.common import get_md5
import datetime

class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/zhaopin/shujuwajue/2/?filterOption=2']

    rules = (
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'zhaopin/.*'),follow=True),
        Rule(LinkExtractor(allow=r'gongsi/.*'),follow=True),
    )

    # 重载方法替代无法重载的parse函数
    # def parse_start_url(self, response):
    #     return []
    #
    # def process_results(self, response, results):
    #     return results



    def parse_item(self, response):

        # i = {}
        # #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        # #i['name'] = response.xpath('//div[@id="name"]').extract()
        # #i['description'] = response.xpath('//div[@id="description"]').extract()
        # return i


        item_loader = LagouItemLoader(item=LagouJobItem(),response=response)
        item_loader.add_css("title",'.job-name > .name::text')
        item_loader.add_value("url",response.url)
        item_loader.add_value("url_object_id",get_md5(response.url))
        item_loader.add_css("salary",'.job_request .salary::text')
        item_loader.add_xpath("job_city", '//*[@class="job_request"]/p/span[2]/text()')
        item_loader.add_xpath("work_years",'//*[@class="job_request"]/p/span[3]/text()')
        item_loader.add_xpath("degree_need",'//*[@class="job_request"]/p/span[4]/text()')
        item_loader.add_xpath("job_type",'//*[@class="job_request"]/p/span[5]/text()')
        item_loader.add_css("publish_time",'.publish_time::text')
        item_loader.add_css("job_advantage",'.job-advantage p::text')
        item_loader.add_css("job_desc",'.job_bt div::text')
        item_loader.add_css("job_addr",'.work_addr')
        item_loader.add_css("company_name",'#job_company dt a img::attr(alt)')
        item_loader.add_css("company_url",'#job_company dt a::attr(href)')
        item_loader.add_css("tags",'.position-label li:text ')
        item_loader.add_value("crawl_time",datetime.datetime.now())

        return item_loader.load_item()

