# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='{{ cookiecutter.repo_name }}',
    version='0.1.0',
    packages=find_packages(),
    entry_points={'scrapy': ['settings = {{ cookiecutter.repo_name }}.settings']},  # noqa
)
