# -*- coding: utf-8 -*-

from scrapy.contrib.spiders.init import InitSpider
import datetime


class SpiderBase(InitSpider):

    def extractor(self, xpathselector, selector):
        """
        Helper function that extract info from xpathselector object
        using the selector constrains.
        """
        val = xpathselector.xpath(selector).extract()
        return val[0] if val else ''

    def response_to_file(self, name, response):
        with open(name, 'wb') as f:
            f.write(response.body)


class CaptchaMixin(object):
    def process_captcha(self, *args, **kwargs):
        raise NotImplementedError(
            'SpiderBaseUtils requires a process_captcha method.'
            )

    def get_captcha(self, *args, **kwargs):
        self.crawler.engine.pause()
        captcha = self.process_captcha(*args, **kwargs)
        self.crawler.engine.unpause()
        return captcha


class ValidationMixin(object):

    def clean_size(self, input_str, size):
        if not len(input_str) == size:
            return False
        return True

    def only_chars(self, value):
        pass

    def only_digits(self, value):
        if value.isdigit():
            return True
        return False

    def clean_all_white_spaces(self, item):
        return ''.join(item.split())

    def clean_line_white_spaces(self, item):
        return item.replace('\n', '').replace('\t', '').replace('\r', '')

    def str2datetime(self, date_time):
        try:
            return datetime.datetime.strptime(date_time, '%d/%m/%Y %H:%M:%S')
        except ValueError:
            return None

    def str2date(self, date):
        try:
            return datetime.datetime.strptime(date, '%d/%m/%Y')
        except ValueError:
            return None


class ItemMixin(ValidationMixin):
    item_class = None
    xpath = None

    def get_item_fields(self):
        return self.item_class.fields

    def extract_item(self, selector):
        return selector.xpath(self.xpath).extract()

    def clean_item(self, extraction):
        return extraction or {}

    def build_item(self, cleaned_data):
        return self.item_class(cleaned_data)

    def update_item(self, old_item, cleaned_data):
        return self.item_class(cleaned_data)

    def process_item(self, selector):
        extraction = self.extract_item(selector)
        cleaned_data = self.clean_item(extraction)
        return self.build_item(cleaned_data)

    def _process_item(self, selector, item_name=None):
        if item_name is None:
            return self.process_item(selector)

        if hasattr(self, 'extract_%s' % item_name):
            extraction = getattr(self, 'extract_%s' % item_name)(selector)
        else:
            extraction = self.extract_item(selector)

        if hasattr(self, 'clean_%s' % item_name):
            cleaned_data = getattr(self, 'clean_%s' % item_name)(extraction)
        else:
            cleaned_data = self.clean_item(extraction)

        if hasattr(self, 'build_%s' % item_name):
            return getattr(self, 'build_%s' % item_name)(cleaned_data)
        else:
            return self.build_item(cleaned_data)


class FieldExampleMixin(object):
    field = None
    default = None

    def get_field(self):
        if self.field is None:
            return self.default
        else:
            return self.field
