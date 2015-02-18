# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


class TecdocRouter(object):
    def is_tecdoc_model(self, model):
        return model._meta.app_label == 'tecdoc'

    def db_for_read(self, model, **hints):
        return 'tecdoc' if self.is_tecdoc_model(model) else None

    def db_for_write(self, model, **hints):
        return 'tecdoc' if self.is_tecdoc_model(model) else None

    def allow_relation(self, obj1, obj2, **hints):
        if self.is_tecdoc_model(obj1) and self.is_tecdoc_model(obj2):
            return True
        return None

    def allow_syncdb(self, db, model):
        if db == 'tecdoc':
            return model._meta.app_label in ['tecdoc',]
        elif self.is_tecdoc_model(model):
            return False
        return None
