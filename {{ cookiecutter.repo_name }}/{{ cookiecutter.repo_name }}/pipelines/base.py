# -*- coding: utf-8 -*-

from ..models import Base
from os.path import basename
from os.path import join
from scrapy.contrib.pipeline.files import FilesPipeline
from scrapy.http import Request
from scrapy.utils.project import get_project_settings as Settings
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import MultipleResultsFound
from sqlalchemy.orm.exc import NoResultFound
from urllib2 import unquote

settings = Settings()


class PostgreSQLMixin(object):
    SETTINGS = settings['POSTGRESQL_DATABASE']

    def __init__(self):
        self.engine = self.get_engine()
        self.create_tables()
        self.Session = sessionmaker(bind=self.engine)

    def create_connection(self):
        return self.Session()

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def get_engine(self):
        return create_engine(URL(**self.SETTINGS))

    def test_connection(self):
        pass


class ModelMixin(object):

    model = None

    def get_model(self):
        if self.model is None:
            raise NotImplementedError(
                'ModelMixin requires a model class.'
                )
        else:
            return self.model


class PipelineAllowedMixin(object):

    pipeline_allowed = None

    def get_pipeline_allowed(self):
        if self.pipeline_allowed is None:
            raise NotImplementedError(
                'PipelineAllowedMixin requires a pipelines_allowed variable.'
                )
        else:
            return self.pipeline_allowed

    def pipeline_is_allowed(self, spider):
        pipeline_allowed = self.get_pipeline_allowed()
        spider_pipelines = getattr(spider, 'pipelines_allowed', [])
        return pipeline_allowed in spider_pipelines


class ItemAllowedMixin(object):
    item_allowed = None

    def get_item_allowed(self):
        if self.item_allowed is None:
            raise NotImplementedError(
                'ItemAllowedMixin requires a items_allowed variable.'
                )
        else:
            return self.item_allowed

    def item_is_allowed(self, item):
        item_allowed = self.get_item_allowed()
        return isinstance(item, item_allowed)


class BasePipeline(PipelineAllowedMixin, ItemAllowedMixin):

    def item_pipeline(self, item, spider):
        raise NotImplementedError(
            'BasePipeline requires an item_pipeline method.'
            )

    def pre_item_pipeline(self, item, spider):
        pass

    def pos_item_pipeline(self, item, spider):
        pass

    def process_item(self, item, spider):

        if not self.pipeline_is_allowed(spider):
            return item

        if not self.item_is_allowed(item):
            return item

        self.pre_item_pipeline(item, spider)
        item = self.item_pipeline(item, spider)
        self.pos_item_pipeline(item, spider)

        return item


class PostgreSQLBasePipeline(PipelineAllowedMixin, ItemAllowedMixin,
                             PostgreSQLMixin):

    def item_pipeline(self, connection, item, spider):
        raise NotImplementedError(
            'BasePipeline requires an item_pipeline method.'
            )

    def pre_item_pipeline(self, connection, item, spider):
        pass

    def pos_item_pipeline(self, connection, item, spider):
        pass

    def process_item(self, item, spider):
        connection = self.create_connection()

        if not self.pipeline_is_allowed(spider):
            return item

        if not self.item_is_allowed(item):
            return item

        self.pre_item_pipeline(connection, item, spider)
        item = self.item_pipeline(connection, item, spider)
        self.pos_item_pipeline(connection, item, spider)

        return item


class BaseDownloadPipeline(FilesPipeline, BasePipeline):
    base_folder = None
    file_attribute = None

    def get_base_folder(self):
        if self.base_folder is None:
            raise NotImplementedError(
                'BaseDownloadPipeline requires a base_folder variable.'
                )
        else:
            return self.base_folder

    def process_item(self, item, spider):

        if not self.pipeline_is_allowed(spider):
            return item

        if not self.item_is_allowed(item):
            return item

        super(FilesPipeline, self).process_item(item, spider)

    def get_file_attribute(self):
        if self.file_attribute is None:
            return self.DEFAULT_FILES_URLS_FIELD
        else:
            return self.file_attribute

    def upload_to(self, filename):
        return join(self.base_folder, filename)

    def file_path(self, request, response=None, info=None):
        filename = basename(unquote(request.url))
        return self.upload_to(filename)

    def get_media_requests(self, item, info):
        return [Request(x) for x in item.get(self.get_file_attribute(), [])]


class ModelPipeline(ModelMixin, PostgreSQLBasePipeline):

    primary_keys_labels = None

    def get_model_pkeys_labels(self):
        if self.primary_keys_labels is None:
            raise NotImplementedError(
                'ModelPipeline requires a primary_keys_labels variable.'
                )
        else:
            return self.primary_keys_labels

    def get_model_primary_key(self, item):
        return dict((k, item[k]) for k in self.get_model_pkeys_labels())

    def check_item_exists(self, connection, item):
        try:
            item_model = connection.query(
                self.get_model()).filter_by(
                **self.get_model_primary_key(item)).one()
            return True
        except MultipleResultsFound, e:
            return True
        except NoResultFound, e:
            return False

    def get_or_create(connection, **kwargs):

        instance = connection.query(self.get_model()).filter_by(**kwargs)
        if instance:
            return instance
        else:
            instance = self.model(**kwargs)
            session.add(instance)
            session.commit()
            return instance

    def item_pipeline(self, connection, item, spider):

        if self.check_item_exists(connection, item):
            return item

        item_model = self.model(**item)

        try:
            connection.add(item_model)
            connection.commit()
        except:
            connection.rollback()
            raise
        finally:
            connection.close()

        return item
