# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from appconf import AppConf


PDF_TYPE = 2

DE_LANG = 1
EN_LANG = 3
RU_LANG = 16


class TecdocConf(AppConf):
    DATABASE = 'tecdoc'
    DB_PREFIX = ''

    LANG_ID = RU_LANG
    APP_ROOT = '.'

    # Host for generation absolute path for images and pdf
    FILE_HOST = 'http://server/'

    CACHE_TIMEOUT = 60 * 60  # one hour
