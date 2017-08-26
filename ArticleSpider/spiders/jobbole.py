# -*- coding: utf-8 -*-
import scrapy
import re

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/110287/']

    def parse(self, response):

        # # 通过xpath语法提取  xpath的用法
        # title =response.xpath('// div[ @ class = "entry-header"]  / h1/text()').extract()[0]
        # create_date = response.xpath('//div[@class="entry-meta"]/p/text()[1]').extract()[0].strip().rstrip(' ·')
        # praise_num = response.xpath('//div[@class="post-adds"]/span/h10/text()').extract()[0]
        # fav_nums = response.xpath('//span[contains(@class,"bookmark-btn")]/text()').extract()[0]
        # match_re = re.match(".*?(\d+).*",fav_nums)
        # if match_re :
        #     fav_nums = match_re.group(1)
        # comment_nums = response.xpath('//a[contains(@href,"#article-comment")]/span/text()').extract()[0]
        # match_re = re.match(".*?(\d+).*",comment_nums)
        # if match_re :
        #     comment_nums = match_re.group(1)
        # content = response.xpath('//div[@class="entry"]').extract()[0]
        # tag_list = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        # tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        # tags = ",".join(tag_list)

        # 通过css选择器提取 css选择器实现字段解析
        title = response.css('div.entry-header h1::text').extract_first()
        create_date = response.css('div.entry-meta p:nth-child(1)::text').extract()[0].strip().rstrip(' ·')
        praise_num = response.css('div.post-adds span h10::text').extract()[0]
        fav_nums = response.css('span[class*="bookmark-btn"]::text').extract()[0]
        match_re = re.match(".*?(\d+).*", fav_nums)
        if match_re:
            fav_nums = match_re.group(1)
        comment_nums = response.css('a[href*="#article-comment"] span::text').extract()[0]
        match_re = re.match(".*?(\d+).*", comment_nums)
        if match_re:
            comment_nums = match_re.group(1)
        content = response.css('div.entry').extract()[0]
        tag_list = response.css("p.entry-meta-hide-on-mobile a::text").extract()
        tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        tags = ",".join(tag_list)



        pass
