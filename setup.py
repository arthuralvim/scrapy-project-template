# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='{{ project_name }}',
    version='1.0',
    packages=find_packages(),
    entry_points={'scrapy': ['settings = {{ project_name }}.settings']},
)
