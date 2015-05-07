# -*- coding: utf-8 -*-

from .constants import ERROR_MSG


class SampleErrorException(Exception):

    def __init__(self, message=None):
        super(SampleErrorException, self).__init__(message)
        self.message = ERROR_MSG
