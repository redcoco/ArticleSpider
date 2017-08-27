# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib import parse
from ArticleSpider.items import JobboleItem
from ArticleSpider.utils.common import get_md5
import datetime

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/page/550/']

    def parse(self, response):

        """
        1.获取文章列表页的文章url并交给scrapy下载后进行解析
        2.获取下一页的url并交给scrapy进行下载，下载完成后交给parse解析
        """

        # 获取文章列表页的文章url并交给scrapy下载后进行解析

        post_nodes = response.css('#archive .floated-thumb .post-thumb a')
        for post_node in post_nodes:
            # 传递meta信息到parse_detail
            image_url = post_node.css('img::attr(src)').extract_first("")
            post_url = post_node.css('::attr(href)').extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse_detail,
                          meta={"front_image_url": image_url})

        # 获取下一页的url并交给scrapy进行下载，下载完成后交给parse解析
        next_url = response.css('.next.page-numbers::attr(href)').extract_first("")
        if next_url:
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse)

    def parse_detail(self, response):
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
        jobbole_item = JobboleItem()
        front_image_url = response.meta.get("front_image_url", "")
        title = response.css('div.entry-header h1::text').extract_first()
        create_date = response.css('div.entry-meta p:nth-child(1)::text').extract()[0].strip().rstrip(' ·')
        praise_num = response.css('div.post-adds span h10::text').extract_first()
        fav_nums = response.css('span[class*="bookmark-btn"]::text').extract()[0]
        match_re = re.match(".*?(\d+).*", fav_nums)
        if match_re:
            fav_nums = int(match_re.group(1))
        else:
            fav_nums = 0
        comment_nums = response.css('a[href*="#article-comment"] span::text').extract()[0]
        match_re = re.match(".*?(\d+).*", comment_nums)
        if match_re:
            comment_nums = int(match_re.group(1))
        else:
            comment_nums = 0
        content = response.css('div.entry').extract()[0]
        tag_list = response.css("p.entry-meta-hide-on-mobile a::text").extract()
        tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        tags = ",".join(tag_list)

        # item设计
        jobbole_item["front_image_url"] = [front_image_url] # 后台解析IMAGES_URLS_FIELD 是一个数组，所以需要转数组
        # jobbole_item["front_image_path"] = 该字段在JobboleImagesPipeline 中定义的
        jobbole_item["url"] = response.url
        jobbole_item["url_object_id"] = get_md5(response.url)
        jobbole_item["title"] = title
        try:
            create_date = datetime.datetime.strftime(create_date,"%Y/%m/%d").date()
        except Exception as e:
            create_date = datetime.datetime.now().date()
        jobbole_item["create_date"] = create_date
        jobbole_item["praise_num"] = praise_num
        jobbole_item["fav_nums"] = fav_nums
        jobbole_item["comment_nums"] = comment_nums
        jobbole_item["content"] = content
        jobbole_item["tags"] = tags

        yield jobbole_item
