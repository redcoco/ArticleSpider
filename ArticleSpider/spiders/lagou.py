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
    start_urls = ['https://www.lagou.com']

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
        item_loader.add_css("tags",'.position-label li::text ')
        item_loader.add_value("crawl_time",datetime.datetime.now())

        item = item_loader.load_item()
        return item

    # def start_requests(self):
    #     # 提交form表单
    #     return [scrapy.Request("https://passport.lagou.com/login/login.html", headers=self.headers, callback=self.login)]
    #
    # def login(self, response):
    #     match_obj = re.match('.*name="_xsrf" value="(.*?)".*', response.text, re.DOTALL)
    #     xsrf = ''
    #     if match_obj:
    #         xsrf = match_obj.group(1)
    #     if xsrf:
    #         post_url = "https://www.zhihu.com/login/phone_num"
    #         post_data = {
    #             "_xsrf": xsrf,
    #             "phone_num": "15995848840",
    #             "password": input("请输入密码\n>>>>>>"),
    #             "captcha": ""
    #         }
    #
    #     import time
    #     t = str(int(time.time() * 1000))
    #     captcha_url = "https://www.zhihu.com/captcha.gif?r={0}&type=login".format(t)
    #     yield scrapy.Request(captcha_url, headers=self.headers, meta={"post_data": post_data},
    #                          callback=self.login_after_captcha)
    #
    # def login_after_captcha(self, response):
    #
    #     with open("captcha.jpg", "wb") as f:
    #         f.write(response.body)
    #         f.close()
    #     from PIL import Image
    #
    #     try:
    #         im = Image.open("captcha.jpg")
    #         im.show()
    #         im.close()
    #     except:
    #         print("图片打开失败\n")
    #     captcha = input("请输入验证码\n>>>>>>")
    #
    #     post_url = "https://www.zhihu.com/login/phone_num"
    #     post_data = response.meta.get("post_data")
    #     post_data["captcha"] = captcha
    #     return [FormRequest(
    #         url=post_url,
    #         formdata=post_data,
    #         headers=self.headers,
    #         callback=self.check_login
    #     )]
    #
    # def check_login(self, response):
    #     # 验证服务器的返回数据判断是否成功
    #     text_json = json.loads(response.text)
    #     if "msg" in text_json and text_json["msg"] == "登录成功":
    #         for url in self.start_urls:
    #             yield scrapy.Request(url, dont_filter=True, headers=self.headers)

