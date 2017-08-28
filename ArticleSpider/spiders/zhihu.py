# -*- coding: utf-8 -*-
import scrapy
from scrapy import FormRequest
import re
import json


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    headers = {
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhihu.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"
    }

    def parse(self, response):
        pass

    def parse_detal(self,response):
        pass


    def start_requests(self):
        # 提交form表单
        return [scrapy.Request("https://www.zhihu.com/#signin",headers=self.headers,callback=self.login)]

    def login(self,response):
        match_obj = re.match('.*name="_xsrf" value="(.*?)".*', response.text, re.DOTALL)
        xsrf = ''
        if match_obj:
            xrsf =  match_obj.group(1)
        if xrsf:
            post_url = "https://www.zhihu.com/login/phone_num"
            post_data = {
                "_xsrf": xsrf,
                "phone_num": "18722366878",
                "password": "admin123"
            }
        return [FormRequest(
            url=post_url,
            formdata=post_data,
            headers=self.headers,
            callback=self.check_login
        )]

    def check_login(self,response):
        # 验证服务器的返回数据判断是否成功
        text_json = json.load(response.text)
        if "msg" in text_json and text_json["msg"] == "登陆成功" :
            for url in self.start_urls:
                yield scrapy.Request(url,dont_filter=True,headers=self.headers,callback=self.parse)
