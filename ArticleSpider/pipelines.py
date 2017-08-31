# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
import codecs
import json
from scrapy.exporters import JsonItemExporter
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class JobboleImagesPipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if "front_image_url" in item:
            for ok, value in results:
                if ok :
                    image_file_path = value["path"]
                else:
                    image_file_path = ""
            item["front_image_path"] = image_file_path

        return item


class JsonFilePipeline(object):
    """
    保存数据到json文件中,自己写的pipeline
    """

    def __init__(self):
        self.file = codecs.open("jobbole.json", "w", encoding="utf-8")

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()


class JsonExporterPipeline(JsonItemExporter):
    """
    继承JsonItemExporter实现使用系统的exportors文件
    """

    def __init__(self):
        self.file = codecs.open("jobboleexport.json", "wb")
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def closed_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect("host", "user", "password", "dbname", charset="utf-8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
                    insert into jobbole () VALUES (%s,%s,%s,%s)
                    """
        self.cursor.execute(insert_sql, (
            item["title"], item["create_date"], item["fav_nums"], item["content"], item["tags"], item["comment_nums"],
            item["praise_num"], item["front_image_url"]))
        self.conn.commit()


class MysqlTwistedPipeline(object):
    """
    异步高并发插入mysql
    """

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            password=settings["MYSQL_PASSWORD"],
            charset='utf-8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)

    def do_insert(self, cursor, item):
        insert_sql,params = item.get_insert_sql()
        self.cursor.execute(insert_sql,params)

        # insert_sql = """
        #                     insert into jobbole () VALUES (%s,%s,%s,%s)
        #                     """
        # self.cursor.execute(insert_sql, (
        #     item["title"], item["create_date"], item["fav_nums"], item["content"], item["tags"], item["comment_nums"],
        #     item["praise_num"], item["front_image_url"]))

    def handle_error(self, failure, item, spider):
        # 处理异步插入语的异常
        print(failure)
