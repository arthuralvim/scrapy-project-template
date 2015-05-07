# -*- coding: utf-8 -*-

from ...items import SpiderJobItem
from ..base import ItemMixin
from ..base import SpiderBase
from decouple import config
from scrapy import log
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import Selector


class LoginMixin(object):
    login = config('login', default='test_login')
    password = config('password', default='test_password')
    login_page = 'login_url'
    login_form_action = 'login_form_action'

    def login(self, response):

        payload = {
            'username': self.login,
            'password': self.password,
        }

        return [
            FormRequest(
                url=self.login_form_action,
                formdata=payload,
                callback=self.check_login_response
            )
        ]

    def get_login_callback(self):
        return self.initial_callback

    def get_login_callback_url(self):
        return self.initial_url

    def check_login_response(self, response):

        if 'logged,' not in response.body:
            self.log('Login failed!', level=log.ERROR)
            return

        return Request(url=self.get_login_callback_url(),
                       callback=self.get_login_callback())


class SearchMixin(object):

    search_page = 'search_url'
    search_form_action = 'search_form_action'

    def prepare_payload(self, response):
        return {}

    def search(self, response):
        search_payload = self.prepare_payload(response)

        return [
            FormRequest(
                url=self.search_form_action,
                formdata=search_payload,
                callback=self.search_results
            )
        ]

    def search_results(self, response):
        if 'results' in response.body:
            return self.extract_item(response)
        else:
            self.log('Search return without results!', level=log.ERROR)
            return


class SampleItemMixin(ItemMixin):
    xpath_sample = "//input[@class='some-class']/@value"

    def extract_sample(self, selector):
        return selector.xpath(self.xpath_declaracao).extract()

    def build_sample(self, cleaned_data):

        fields = SpiderJobItem.fields

        fields['job_id'] = cleaned_data[0]

        return SpiderJobItem(fields)


class ExtractMixin(SampleItemMixin):

    def extract_item(self, response):
        hxs = Selector(response)
        sample = self._process_item(hxs, 'sample')
        yield sample


class SampleSpiderBase(LoginMixin, SearchMixin, ExtractMixin, SpiderBase):

    initial_url = 'initial_url'

    allowed_domains = [
        'domain.com',
    ]

    start_urls = [
        'domain.com',
    ]

    def init_request(self):
        hdrs = {'referer': self.initial_url}
        return Request(url=self.login_page, callback=self.login, headers=hdrs)

    def get_login_callback(self):
        return self.search

    def get_login_callback_url(self):
        return self.search_page
