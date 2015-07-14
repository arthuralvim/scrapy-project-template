# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from scrapy.utils.project import get_project_settings as Settings
settings = Settings()

engine = create_engine(settings['POSTGRES_URL'])
Base = declarative_base(engine)
