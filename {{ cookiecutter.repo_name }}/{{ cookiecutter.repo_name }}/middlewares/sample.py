# -*- coding: utf-8 -*-

from scrapy import signals
import os

__all__ = ['SpiderJobMiddleware', ]


class SpiderJobMiddleware(object):

    def __init__(self, crawler):
        self.crawler = crawler
        crawler.signals.connect(self.close_spider, signals.spider_closed)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def close_spider(self, spider, reason):
        stats = self.crawler.stats.get_stats()
        jobid = self.get_jobid()
        self.update_job_stats(jobid, stats)

    def get_jobid(self):
        try:
            return os.environ['SCRAPY_JOB']
        except Exception:
            return None

    def update_job_stats(self, jobid, stats):
        pass
