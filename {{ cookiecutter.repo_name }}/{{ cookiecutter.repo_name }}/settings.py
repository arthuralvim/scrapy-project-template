# -*- coding: utf-8 -*-

# Scrapy - {{ cookiecutter.repo_name }}

from decouple import config
from unipath import Path

PROJECT_NAME = '{{ cookiecutter.repo_name }}'
PROJECT_PATH = Path(__file__).absolute().ancestor(1)
SPIDER_MODULES = ['{{ cookiecutter.repo_name }}.spiders']
NEWSPIDER_MODULE = '{{ cookiecutter.repo_name }}.spiders'
BOT_NAME = config('BOT_NAME', default='{{ cookiecutter.repo_name }}')
USER_AGENT = config('USER_AGENT', default='Spider - {{ cookiecutter.repo_name }}')

# LOGS

LOG_ENABLED = config('LOG_ENABLED', default=False, cast=bool)
LOG_FILE = config('LOG_FILE', default='scrapy-{{ cookiecutter.repo_name }}.log')

# AUTOTHROTTLE

AUTOTHROTTLE_ENABLED = config('AUTOTHROTTLE_ENABLED', default=True, cast=bool)
AUTOTHROTTLE_START_DELAY = config('AUTOTHROTTLE_START_DELAY', default=5.0,
                                  cast=float)
AUTOTHROTTLE_MAX_DELAY = config('AUTOTHROTTLE_MAX_DELAY', default=15.0,
                                cast=float)
AUTOTHROTTLE_DEBUG = config('AUTOTHROTTLE_DEBUG', default=False, cast=bool)

# CONCURRENCY

CONCURRENT_REQUESTS = config('CONCURRENT_REQUESTS', default=16, cast=int)
CONCURRENT_REQUESTS_PER_IP = config('CONCURRENT_REQUESTS_PER_IP', default=2,
                                    cast=int)

# EXTENSIONS

# EXTENSIONS = {
#     'scrapy.contrib.feedexport.FeedExporter': None,
# }

# MIDDLEWARES

# SPIDER_MIDDLEWARES = {
#     '{{ cookiecutter.repo_name }}.middlewares.SpiderJobMiddleware': 500,
# }

# DATABASE

# POSTGRESQL_DATABASE = {
#     'drivername': config('DB_DRIVER', default='postgres'),
#     'host': config('DB_HOST', default='localhost'),
#     'port': config('DB_PORT', default='5432'),
#     'username': config('DB_USER'),
#     'password': config('DB_PASS'),
#     'database': config('DB_NAME'),
# }

# PIPELINES

# ITEM_PIPELINES = {
#     '{{ cookiecutter.repo_name }}.pipelines.SamplePipeline': 500,
# }

# FILE STORAGE

SPIDER_DOWNLOAD_DIR = config('DOWNLOAD_DIR',
                             default=PROJECT_PATH.child('media'))
FILES_STORE = config('FILES_STORE', default=SPIDER_DOWNLOAD_DIR)

# SENTRY

# if config('USE_SENTRY', default=False, cast=bool):
#     SENTRY_DSN = config('SENTRY_DSN')
#     EXTENSIONS = {
#         'scrapy_sentry.extensions.Errors': 10,
#     }
