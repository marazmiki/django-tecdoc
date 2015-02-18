# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.db import models
from tecdoc.conf import TecdocConf as td_conf, PDF_TYPE
from tecdoc.utils import clean_number


Q = models.Q


class TecdocManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super(TecdocManager, self).get_queryset(*args, **kwargs)\
            .using(td_conf.DATABASE)


class TecdocManagerWithDes(TecdocManager):
    def get_queryset(self, *args, **kwargs):
        query = super(TecdocManagerWithDes, self).get_queryset(*args, **kwargs)
        query = query.filter(designation__lang=td_conf.LANG_ID)
        return query.select_related('designation__description')


class DesignationManager(TecdocManager):
    def get_queryset(self, *args, **kwargs):
        return (super(DesignationManager, self).get_queryset(*args, **kwargs)
                                               .filter(lang=td_conf.LANG_ID)
                                               .select_related('description')
                                               )
class DesignationQuerySet(models.QuerySet):
    def filter(self, *args, **kwargs):
        kwargs.update(lang=td_conf.LANG_ID)
        return super(DesignationQuerySet, self).filter(*args, **kwargs).select_related('description')
    # def get_queryset(self, *args, **kwargs):
    #     return (super(DesignationManager, self).get_queryset(*args, **kwargs)
    #                                            .filter(lang=td_conf.LANG_ID)
    #                                            .select_related('description')
    #                                            )




class CarModelManager(TecdocManagerWithDes):

    def get_queryset(self, *args, **kwargs):
        return super(CarModelManager, self).get_queryset(*args, **kwargs).\
            select_related('manufacturer', 'designation__description').\
            distinct()

    def get_models(self, manufacturer, date_min=None, date_max=None,
                   search_text=None):

        query = self.filter(manufacturer=manufacturer)

        if date_min:
             # TODO
             pass

        if date_max:
             pass

        if search_text:
             query.filter(designation__description__text__icontains=search_text)

        return query

class EngineManager(TecdocManager):
    def get_queryset(self, *args, **kwargs):
        return (super(EngineManager, self).get_queryset(*args, **kwargs)
                                          .filter(fuel_des__lang=td_conf.LANG_ID)
                                          .select_related('manufacturer',
                                                          'fuel_des__description')
               )

class CarTypeManager(TecdocManagerWithDes):

    def get_queryset(self, *args, **kwargs):
        return (super(CarTypeManager, self).get_queryset(*args, **kwargs)
                                           .filter(model__designation__lang=td_conf.LANG_ID,
                                                   full_designation__lang=td_conf.LANG_ID,
                                                   drive_des__lang=td_conf.LANG_ID,
                                                   body_des__lang=td_conf.LANG_ID,
                                                   designation__description__text__isnull=False)
                                           .select_related('model__manufacturer',
                                                           'model__designation__description',
                                                           'full_designation__description',
                                                           'designation__description',
                                                           'drive_des__description',
                                                           'body_des__description')
                                           .prefetch_related('engines'))

class PartCriteriaManager(TecdocManagerWithDes):
    def get_queryset(self, *args, **kwargs):
        query = super(PartCriteriaManager, self).get_queryset(*args, **kwargs)
        query = query.filter(criteria__short_designation__lang=td_conf.LANG_ID,
                             criteria__designation__lang=td_conf.LANG_ID)
        return query.select_related('designation__description',
                                    'criteria__short_designation__description',
                                    'criteria__designation__description')

class CriteriaManager(TecdocManagerWithDes):
    def get_queryset(self, *args, **kwargs):
        query = super(CriteriaManager, self).get_queryset(*args, **kwargs)
        query = query.filter(short_designation__lang=td_conf.LANG_ID)
        return query.select_related('designation__description',
                                    'short_designation__description')

class ImageManager(TecdocManager):
    def get_queryset(self, *args, **kwargs):
        return (super(ImageManager, self).get_queryset(*args, **kwargs)
                                         .filter(lang__in=(td_conf.LANG_ID, 255))
                                         .exclude(type=PDF_TYPE)
                                               )
class PdfManager(TecdocManager):
    def get_queryset(self, *args, **kwargs):
        return (super(PdfManager, self).get_queryset(*args, **kwargs)
                                       .filter(lang__in=(td_conf.LANG_ID, 255),
                                               type=PDF_TYPE)
               )

class PartManager(TecdocManagerWithDes):
    def get_queryset(self, *args, **kwargs):
        query = super(PartManager, self).get_queryset(*args, **kwargs)
        query = query.select_related('designation__description',
                                     'supplier')

        query = query.prefetch_related('analogs', 'images')
        return query

    def lookup(self, number, manufacturer=None):
        from tecdoc.models import PartAnalog
        query = Q(search_number=clean_number(number))
        if manufacturer:
            if isinstance(manufacturer, int):
                query &= Q(part__supplier=manufacturer) | Q(brand=manufacturer)
            elif hasattr(manufacturer, '__iter__'):
                query &= Q(part__supplier__title__in=manufacturer) | Q(brand__title__in=manufacturer)
            else:
                query &= Q(part__supplier__title=manufacturer) | Q(brand__title=manufacturer)
        return PartAnalog.objects.filter(query)


class GroupManager(TecdocManagerWithDes):
    def get_queryset(self, *args, **kwargs):
        return super(GroupManager, self).get_queryset(*args, **kwargs)\
            .filter(standard__lang=td_conf.LANG_ID,
                    assembly__lang=td_conf.LANG_ID,
                    intended__lang=td_conf.LANG_ID)\
            .select_related('designation__description',
                            'standard__description',
                            'assembly__description',
                            'intended__description')
