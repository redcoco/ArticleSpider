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
from w3lib.html import remove_tags
from ArticleSpider.es_utils.es_types import ArticleType
from w3lib.html import remove_tags


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


def remove_splash(value):
    # 去掉斜杠
    return value.replace("/", "")


from elasticsearch_dsl.connections import connections
es = connections.create_connection(ArticleType._doc_type.using)


def gen_suggests(index, info_tuple):
    # 生成es搜索建议字段
    used_words = set()
    suggests = []
    for text, weight in info_tuple:
        if text:
            # 调用es的analazyer分词
            words = es.indices.analyze(index=index, analyzer="ik_max_word", params={"filter": ["lowercase"]},body=text)
            analyzed_words = set([r["token"] for r in words["tokens"] if len(r["token"]) > 1])
            new_words = analyzed_words - used_words
        else:
            new_words = set()
        if new_words:
            suggests.append({"input": list(new_words), "weight": weight})
        return suggests


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

    # 为了实现多item保存到es
    def save_to_es(self):
        article = ArticleType()
        article.title = self["title"]
        article.create_date = self["create_date"]
        article.content = remove_tags(self["content"])
        article.front_image_url = self["front_image_url"]
        if "front_image_path" in self:
            article.front_image_path = self["front_image_path"]
        if "praise_num" in self:
            article.praise_num = self["praise_num"]
        if "fav_nums" in self:
            article.fav_nums = self["fav_nums"]
        if "comment_nums" in self:
            article.comment_nums = self["comment_nums"]
        article.url = self["url"]
        article.tags = self["tags"]
        article.meta.id = self["url_object_id"]

        # 生成搜索建议词
        article.suggest = gen_suggests(ArticleType._doc_type.index, ((article.title, 10), (article.tags, 7)))
        article.save()


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
            self["zhihu_id"][0], "".join(self["title"]), "".join(self["topics"]), self["url"][0],
            "".join(self["content"]),
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
            self["zhihu_id"][0], "".join(self["title"]), "".join(self["topics"]), self["url"][0],
            "".join(self["content"]),
            ",".join(self["tags"]), int(self["comment_nums"]))
        return insert_sql, params


class LagouItemLoader(ItemLoader):
    # 自定义itemloader
    default_output_processor = TakeFirst()  # 所有的字段取第一个


def handle_jobaddr(value):
    # 去除查看地图 \n
    addr_list = value.split("\n")
    addr_list = [item.strip() for item in addr_list if item.strip() != "查看地图"]
    return "".join(addr_list)


class LagouJobItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    salary = scrapy.Field()
    job_city = scrapy.Field(
        input_processor=MapCompose(remove_splash),
    )
    work_years = scrapy.Field(
        input_processor=MapCompose(remove_splash),
    )
    degree_need = scrapy.Field(
        input_processor=MapCompose(remove_splash),
    )
    job_type = scrapy.Field()
    publish_time = scrapy.Field()
    job_advantage = scrapy.Field()
    job_desc = scrapy.Field()
    job_addr = scrapy.Field(
        input_processor=MapCompose(remove_tags, handle_jobaddr),
    )
    company_name = scrapy.Field()
    company_url = scrapy.Field()
    tags = scrapy.Field(
        input_processor=Join(","),
    )
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
        insert into lagou_job (url,title,job_addr,work_years,job_desc) VALUES (%s,%s,%s,%s)
        """
        params = (
            self["url"][0], "".join(self["title"]), "".join(self["job_addr"]), self["work_years"][0],
            "".join(self["content"]))
        return insert_sql, params
