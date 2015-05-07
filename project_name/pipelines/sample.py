# -*- coding: utf-8 -*-

from ..items import SpiderJobItem
from ..models import SpiderJob
from .base import BaseDownloadPipeline
from .base import ModelPipeline

__all__ = ['SampleFilePipeline', 'SamplePipeline', ]


class SampleFilePipeline(BaseDownloadPipeline):

    pipeline_allowed = 'sample'
    item_allowed = SpiderJobItem
    base_folder = 'sample'
    file_attribute = 'arquivo'


class SamplePipeline(ModelPipeline):

    model = SpiderJob
    pipeline_allowed = 'sample'
    item_allowed = SpiderJobItem
    primary_keys_labels = ['job_id', ]
