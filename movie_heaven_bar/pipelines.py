# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import logging
import redis
from scrapy.exceptions import NotConfigured


class MovieHeavenBarPipeline(object):
    def __init__(self, host, port, db, user, passwd):
        self.host = host
        self.port = port
        self.db = db
        self.user = user
        self.passwd = passwd

    # reference: doc.scrapy.org/en/latest/topics/item-pipeline.html#from_crawler
    @classmethod
    def from_crawler(cls, crawler):
        db_settings = crawler.settings.getdict('MYSQL_SETTINGS')
        if not db_settings:
            raise NotConfigured
        host = db_settings['DB_HOST']
        port = db_settings['DB_PORT']
        db = db_settings['DB_DB']
        user = db_settings['DB_USER']
        passwd = db_settings['DB_PASSWD']
        return cls(host, port, db, user, passwd)

    def open_spider(self, spider):
        # mysql connection
        self.conn = pymysql.connect(
                                       host=self.host,
                                       port=self.port,
                                       db=self.db,
                                       user=self.user,
                                       passwd=self.passwd,
                                       charset='utf8',
                                       use_unicode=True,
                                   )
        self.cursor = self.conn.cursor()

    def save_to_mysql(self, item, spider):
        save_sql = 'INSERT INTO newest_movie(movie_link, movie_name, movie_director, movie_actors, movie_publish_date, movie_score, movie_download_link, movie_hash) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
        try:
            logging.log(logging.INFO, '***************** commit to mysql ***************** ')
            self.cursor.execute(save_sql, (
                                           item.get('movie_link'),
                                           item.get('movie_name'),
                                           item.get('movie_director'),
                                           item.get('movie_actors'),
                                           item.get('movie_publish_date'),
                                           item.get('movie_score'),
                                           item.get('movie_download_link'),
                                           item.get('movie_hash'),
                                          )
                               )
            self.conn.commit()
            return item
        except Exception as e:
            logging.log(logging.ERROR, f'commit to mysql error: {e}')

    def process_item(self, item, spider):
        self.save_to_mysql(item, spider)

    def close_spider(self, spider):
        self.conn.close()
