# -*- coding: utf-8 -*-
from elasticsearch_dsl import DocType, Date, Nested, Boolean, analyzer, InnerObjectWrapper, Completion, Keyword, Text, \
    Integer
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer

class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}

ik_analyzer = CustomAnalyzer("ik_max_word",filter = ["lowercase"])


connections.create_connection(hosts=["localhost"])


class ArticleType(DocType):
    """
    es初始化数据库表,index设置doctype
    """
    suggest = Completion(analyzer=ik_analyzer)
    front_image_url = Keyword()
    front_image_path = Keyword()
    url = Keyword()
    url_object_id = Keyword()
    title = Text(analyzer="ik_max_word")
    create_date = Date()
    praise_num = Integer()
    fav_nums = Integer()
    comment_nums = Integer()
    content = Text(analyzer="ik_max_word")
    tags = Text(analyzer="ik_max_word")

    class Meta:
        index = "jobbole"
        doc_type = "article"


if __name__ == "__main__":
    ArticleType.init()
