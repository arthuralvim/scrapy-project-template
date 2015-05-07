# -*- coding: utf-8 -*-

from scrapy import Item
from scrapy import Field

__all__ = ['SpiderJobItem', ]


class SpiderJobItem(Item):
    job_id = Field()
