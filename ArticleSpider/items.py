# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join
import datetime
from scrapy.loader import ItemLoader
import re


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def date_cov(value):
    try:
        create_date = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_date = datetime.datetime.now().date()
    return str(create_date)


def get_nums(value):
    match_re = re.match(".*?(\d+).*", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0


def remove_comment_tags(value):
    if "评论" in value:
        return ""
    else:
        return value


def return_orgin(value):
    return value


class JobboleItemLoader(ItemLoader):
    # 自定义itemloader
    default_output_processor = TakeFirst()  # 所有的字段取第一个


class JobboleItem(scrapy.Item):
    # items设计
    front_image_url = scrapy.Field(
        output_processor=MapCompose(lambda x: x)
    )
    front_image_path = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    title = scrapy.Field()
    create_date = scrapy.Field(
        input_processor=MapCompose(date_cov)
    )
    praise_num = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    fav_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    comment_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    content = scrapy.Field()
    tags = scrapy.Field(
        input_processor=MapCompose(remove_comment_tags),
        out_processor=Join(',')
    )

    def get_insert_sql(self):
        insert_sql = """
        insert into jobbole (content,comment_nums,url) VALUES (%s,%s,%s,%s)
        """
        params = (self["url"][0], "".join(self["content"]), ",".join(self["tags"]), int(self["comment_nums"]))
        return insert_sql, params


class ZhihuQuestionItem(scrapy.Item):
    zhihu_id = scrapy.Field()
    topics = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    answer_num = scrapy.Field()
    comments_num = scrapy.Field()
    watch_user_num = scrapy.Field()

    # click_num = scrapy.Field()
    # crawl_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
        insert into zhihu_question (zhihu_id,topics,url,title,content) VALUES (%s,%s,%s,%s)
        """
        params = (
        self["zhihu_id"][0], "".join(self["title"]), "".join(self["topics"]), self["url"][0], "".join(self["content"]),
        ",".join(self["tags"]), int(self["comment_nums"]))
        return insert_sql, params


class ZhihuAnswerItem(scrapy.Item):
    zhihu_id = scrapy.Field()
    url = scrapy.Field()
    question_id = scrapy.Field()
    author_id = scrapy.Field()
    content = scrapy.Field()
    parise_num = scrapy.Field()
    comments_num = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
        insert into zhihu_answer (zhihu_id,topics,url,title,content) VALUES (%s,%s,%s,%s)
        """
        params = (
        self["zhihu_id"][0], "".join(self["title"]), "".join(self["topics"]), self["url"][0], "".join(self["content"]),
        ",".join(self["tags"]), int(self["comment_nums"]))
        return insert_sql, params

class LagouItemLoader(ItemLoader):
    # 自定义itemloader
    default_output_processor = TakeFirst()  # 所有的字段取第一个


class LagouJobItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    salary = scrapy.Field()
    job_city = scrapy.Field()
    work_years = scrapy.Field()
    degree_need = scrapy.Field()
    job_type = scrapy.Field()
    publish_time = scrapy.Field()
    job_advantage = scrapy.Field()
    job_desc = scrapy.Field()
    job_addr = scrapy.Field()
    company_name = scrapy.Field()
    company_url = scrapy.Field()
    tags = scrapy.Field()
    crawl_time = scrapy.Field()

