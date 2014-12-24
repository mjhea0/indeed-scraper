# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import sqlite3
from os import path

from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy.utils.markup import replace_escape_chars, remove_tags


class IndeedPipeline(object):

    def process_item(self, item, spider):
        i = item['summary'][0]
        i = remove_tags(i)
        i = replace_escape_chars(i)
        item['summary'][0] = i

        i = item['job_title'][0]
        i = remove_tags(i)
        i = replace_escape_chars(i)
        item['job_title'][0] = i

        return item


class SQLiteStorePipeline(object):

    filename = 'data.sqlite'

    def __init__(self):
        self.conn = None
        dispatcher.connect(self.initialize, signals.engine_started)
        dispatcher.connect(self.finalize, signals.engine_stopped)

    def process_item(self, item, domain):
        try:
            self.conn.execute("""
                INSERT INTO jobs
                (job_title, link_url, location, company,
                    summary, source, found_date, source_url,
                    source_page_body, crawl_timestamp, crawl_url)
                values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (
                item['job_title'][0],
                item['link_url'][0],
                item['location'][0],
                item['company'][0],
                item['summary'][0],
                item['source'][0],
                item['found_date'][0],
                item['source_url'],
                item['source_page_body'],
                item['crawl_timestamp'],
                item['crawl_url'])
            )

        except:
            print 'Error!'
        return item

    def initialize(self):
        if path.exists(self.filename):
            self.conn = sqlite3.connect(self.filename)
        else:
            self.conn = self.create_table(self.filename)

    def finalize(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
            self.conn = None

    def create_table(self, filename):
        conn = sqlite3.connect(filename)
        conn.execute(
            """
            CREATE TABLE jobs
            (id INTEGER primary key, job_title TEXT, link_url TEXT
             location TEXT, company TEXT, summary TEXT, source TEXT,
             found_date TEXT, source_url TEXT, source_page_body TEXT,
             crawl_timestamp TEXT, crawl_url TEXT)
            """
        )
        conn.commit()
        return conn
