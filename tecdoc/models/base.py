# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from tecdoc.conf import TecdocConf as tdsettings
from tecdoc.managers import TecdocManager, DesignationManager


class TecdocModel(models.Model):
    objects = TecdocManager()

    class Meta:
        abstract = True
        managed = False
        app_label = 'tecdoc'


@python_2_unicode_compatible
class Description(TecdocModel):
    id = models.AutoField(_('ID'), primary_key=True, db_column='TEX_ID')
    text = models.TextField(_('Текст'), db_column='TEX_TEXT')

    class Meta(TecdocModel.Meta):
        db_table = tdsettings.DB_PREFIX + 'DES_TEXTS'
        verbose_name = _('text')

    def __str__(self):
        return self.text


@python_2_unicode_compatible
class Text(TecdocModel):
    id = models.AutoField(_('ID'), primary_key=True, db_column='TMT_ID')
    text = models.TextField(_('Текст'), db_column='TMT_TEXT', null=True)

    class Meta(TecdocModel.Meta):
        db_table = tdsettings.DB_PREFIX + 'TEXT_MODULE_TEXTS'

    def __str__(self):
        return self.text


class Language(TecdocModel):

    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='LNG_ID')

    designation = models.ForeignKey('tecdoc.Designation',
                                    verbose_name=u'Обозначение',
                                    db_column='LNG_DES_ID',
                                    blank=True, null=True)

    iso_code = models.CharField(u'Код ISO2', max_length=6,
                                db_column='LNG_ISO2',
                                blank=True, null=True)

    codepage = models.CharField(u'Кодировка', max_length=30,
                                db_column='LNG_CODEPAGE',
                                blank=True, null=True)

    class Meta(TecdocModel.Meta):
        db_table = tdsettings.DB_PREFIX + 'LANGUAGES'


class DesignationBase(TecdocModel):

    objects = DesignationManager()

    class Meta(TecdocModel.Meta):
        abstract = True

    def __unicode__(self):
        return self.description.text or '-'


class TextModule(DesignationBase):
    # XXX not a key
    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='TMO_ID')

    lang = models.ForeignKey(Language,
                             verbose_name=u'Язык',
                             related_name='+',
                             db_column='TMO_LNG_ID')

    description = models.ForeignKey(Text,
                                    verbose_name=u'Описание',
                                    db_column='TMO_TMT_ID')

    class Meta(DesignationBase.Meta):
        db_table = tdsettings.DB_PREFIX + 'TEXT_MODULES'




class Designation(DesignationBase):

    # XXX not a key
    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='DES_ID')

    lang = models.ForeignKey(Language,
                             verbose_name=u'Язык',
                             related_name='+',
                             db_column='DES_LNG_ID')

    description = models.ForeignKey(Description,
                                    verbose_name=u'Описание',
                                    db_column='DES_TEX_ID')

    class Meta(DesignationBase.Meta):
        db_table = tdsettings.DB_PREFIX + 'DESIGNATIONS'


class CountryDesignation(DesignationBase):

    # XXX not a key
    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='CDS_ID')

    lang = models.ForeignKey(Language,
                             verbose_name=u'Язык',
                             db_column='CDS_LNG_ID')

    description = models.ForeignKey(Description,
                                    verbose_name=u'Описание',
                                    db_column='CDS_TEX_ID')

    class Meta(DesignationBase.Meta):
        db_table = tdsettings.DB_PREFIX + 'COUNTRY_DESIGNATIONS'
