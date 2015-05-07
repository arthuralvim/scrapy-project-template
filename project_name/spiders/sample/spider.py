# -*- coding: utf-8 -*-

from .base import SampleSpiderBase
from scrapy.exceptions import CloseSpider

__all__ = ['SampleLoginSpider']


class SampleLoginSpider(SampleSpiderBase):

    name = 'sample'
    pipelines_allowed = ['sample', ]

    def __init__(self, some_arg=None, arg_required=None, *args, **kwargs):
        super(SampleLoginSpider, self).__init__(*args, **kwargs)

        self.some_arg = some_arg
        self.arg_required = arg_required

        if not self.arg_required:
            raise CloseSpider('Close spider message!')
