# -*- coding: utf-8 -*-

from .base import Base
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String

__all__ = ['SpiderJob', ]


class SpiderJob(Base):
    """
    Save all spider stats

    'log_count/DEBUG': 7,
    'scheduler/dequeued': 4,
    'log_count/INFO': 7,
    'downloader/response_count': 4,
    'downloader/response_status_count/200': 4,
    'response_received_count': 4,
    'scheduler/enqueued/memory': 4,
    'downloader/response_bytes': 26189,
    'finish_reason': 'finished',
    'start_time': datetime.datetime(2015, 4, 16, 14, 33, 8, 513948),
    'scheduler/dequeued/memory': 4,
    'scheduler/enqueued': 4,
    'finish_time': datetime.datetime(2015, 4, 16, 14, 33, 10, 418879),
    'downloader/request_bytes': 2074,
    'request_depth_max': 3,
    'downloader/request_method_count/GET': 2,
    'item_scraped_count': 1,
    'downloader/request_count': 4,
    'downloader/request_method_count/POST': 2
    """

    __tablename__ = "spider_job"

    id = Column(Integer, primary_key=True)
    job_id = Column('job_id', Integer, nullable=True)

    def __repr__(self):
        return u'<SpiderJob id:{0}>'.format(self.job_id)
