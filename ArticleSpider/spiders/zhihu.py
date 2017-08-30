# -*- coding: utf-8 -*-
import scrapy
from scrapy import FormRequest
import re
import json
from urllib.parse import urljoin
from scrapy.loader import ItemLoader
from ArticleSpider.items import ZhihuAnswerItem,ZhihuQuestionItem
import time


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/']

    headers = {
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhihu.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"
    }

    def parse(self, response):
        """
        提取出html元素的所有url，并跟踪这些url进一步处理，如果url含有question
        """
        all_urls = response.css("a::attr(href)").extract()
        all_urls = [urljoin(response.url, url) for url in all_urls]
        all_urls = filter(lambda x: True if x.startswith("https") else False, all_urls)
        for url in all_urls:
            # if url.startswith("https")
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", url)
            if match_obj:
                request_url = match_obj.group(1)
                question_id = match_obj.group(2)
                yield scrapy.Request(request_url, headers=self.headers, meta={"question_id":question_id},callback=self.parse_question)

    def parse_question(self, response):
        # 处理quetion页面

        if "QuestionHeader-title" in response.text:
            #处理知乎新版本
            item_load = ItemLoader(item=ZhihuQuestionItem(),response=response)
            item_load.add_css("title",'QuestionHeader-title::text')
            item_load.add_css("content",'QuestionHeader-detail')
            item_load.add_value("url",response.url)
            item_load.add_value("zhihu_id",response.meta.get("question_id"))
            item_load.add_css("answer_num",'.List-headerText span::text')
            item_load.add_css("comments_num",'.QuestionHeader-actions button::text')
            item_load.add_css("watch_user_num",'.NumberBoard-value::text')
            item_load.add_css("topics",'.QuestionHeader-topics .Popover::text')
            # item_load.add_css("click_num",'')
            # item_load.add_value("crawl_time",time.time.now())
            question_item = item_load.load_item()
        else:
            #处理老版本
            item_load = ItemLoader(item=ZhihuQuestionItem(), response=response)
            item_load.add_value("zhihu_id", response.meta.get("question_id"))
            item_load.add_value("url", response.url)
            item_load.add_css("title", '.zh-question-title h2 a::text')
            item_load.add_css("content",'#zh-question-detail')
            item_load.add_css("answer_num",'#zh-question-answer-num::text')
            item_load.add_css("comments_num",'#zh-question-meta-wrap a[name="addcomment"]::text')
            item_load.add_css("watch_user_num",'#zh-question-side-header-wrap::text')
            item_load.add_css("topics",'.zm-tag-editor-labels a::text')
            question_item = item_load.load_item()



    def get_captcha(self):
        import time
        t = str(int(time.time() * 1000))
        captcha_url = "https://www.zhihu.com/captcha.gif?r={0}&type=login".format(t)
        t = scrapy.Request(captcha_url, headers=self.headers)

    def start_requests(self):
        # 提交form表单
        return [scrapy.Request("https://www.zhihu.com/#signin", headers=self.headers, callback=self.login)]

    def login(self, response):
        match_obj = re.match('.*name="_xsrf" value="(.*?)".*', response.text, re.DOTALL)
        xsrf = ''
        if match_obj:
            xsrf = match_obj.group(1)
        if xsrf:
            post_url = "https://www.zhihu.com/login/phone_num"
            post_data = {
                "_xsrf": xsrf,
                "phone_num": "15995848840",
                "password": input("请输入密码\n>>>>>>"),
                "captcha": ""
            }

        import time
        t = str(int(time.time() * 1000))
        captcha_url = "https://www.zhihu.com/captcha.gif?r={0}&type=login".format(t)
        yield scrapy.Request(captcha_url, headers=self.headers, meta={"post_data": post_data},
                             callback=self.login_after_captcha)

    def login_after_captcha(self, response):

        with open("captcha.jpg", "wb") as f:
            f.write(response.body)
            f.close()
        from PIL import Image

        try:
            im = Image.open("captcha.jpg")
            im.show()
            im.close()
        except:
            pass
        captcha = input("请输入验证码\n>>>>>>")

        post_url = "https://www.zhihu.com/login/phone_num"
        post_data = response.meta.get("post_data")
        post_data["captcha"] = captcha
        return [FormRequest(
            url=post_url,
            formdata=post_data,
            headers=self.headers,
            callback=self.check_login
        )]

    def check_login(self, response):
        # 验证服务器的返回数据判断是否成功
        text_json = json.loads(response.text)
        if "msg" in text_json and text_json["msg"] == "登录成功":
            for url in self.start_urls:
                yield scrapy.Request(url, dont_filter=True, headers=self.headers)
