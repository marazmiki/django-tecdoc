# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.utils import six
from tecdoc.models import (Manufacturer, Brand, Supplier, CarModel, CarType,
                           Engine, Country, Part, Description, Text,
                           CarSection)


def production_date(value):
    if not value:
        return 'n/a'

    value = six.text_type(value)
    year, month = value[:4], value[4:]

    return '{}/{}'.format(month, year)


class TecdocAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        return []


class EngineAdmin(TecdocAdmin):
    list_display = ['to_string', 'col_production',
                    'power_hp_from', 'power_hp_upto']
    list_filter = ['manufacturer']
    search_fields = ['manufacturer__title', 'manufacturer__code', 'code']
    readonly_fields = ['code', 'manufacturer', 'production_start',
                       'production_end', 'power_kw_from', 'power_kw_upto',
                       'power_hp_from', 'power_hp_upto']
    fieldsets = (
        (None, {'fields': ['manufacturer', 'code']}),
        (_('Production'), {'fields': ['production_start', 'production_end']}),
        (_('Power'), {'fields': [('power_kw_from', 'power_kw_upto'),
                                 ('power_hp_from', 'power_hp_upto')]}),
    )

    def col_production(self, engine):
        if not engine.production_start and not engine.production_end:
            return 'n/a'
        if engine.production_start and not engine.production_end:
            return 'from {}'.format(production_date(engine.production_start))
        if engine.production_start and engine.production_end:
            return 'from {} to {}'.format(
                production_date(engine.production_start),
                production_date(engine.production_end),
            )
        else:
            return 'to {}'.format(production_date(engine.production_end))
    col_production.short_description = _('production years')

    def to_string(self, engine):
        return '{manufacturer} {code}'.format(manufacturer=engine.manufacturer,
                                              code=engine.code)


class CarModelAdmin(TecdocAdmin):
    search_fields = ['manufacturer__title', 'designation__description__text']
    readonly_fields = ['manufacturer', 'designation', 'production_start',
                       'production_end', 'for_car', 'for_truck']
    list_display = ['to_string', 'col_production_start', 'col_production_end',
                    'col_for_car', 'col_for_truck']

    def col_production_start(self, car_model):
        return production_date(car_model.production_start)

    def col_production_end(self, car_model):
        return production_date(car_model.production_end)

    def col_for_car(self, car_model):
        return car_model.for_car == '1'

    def col_for_truck(self, car_model):
        return car_model.for_truck == '1'

    def to_string(self, car_model):
        return '{manufacturer} {designation}'.format(
            manufacturer=car_model.manufacturer,
            designation=car_model.designation
        )

    col_production_end.short_description = _('production end')
    col_production_start.short_description = _('production start')

    col_for_car.boolean = True
    col_for_car.short_description = _('for car')

    col_for_truck.boolean = True
    col_for_truck.short_description = _('for truck')


admin.site.register(Engine, EngineAdmin)
admin.site.register(CarModel, CarModelAdmin)


admin.site.register(Manufacturer, TecdocAdmin)
admin.site.register(Brand, TecdocAdmin)
admin.site.register(Supplier, TecdocAdmin)

admin.site.register(CarType, TecdocAdmin)

admin.site.register(Part, TecdocAdmin)
admin.site.register(Country, TecdocAdmin)
admin.site.register(Description, TecdocAdmin)
admin.site.register(Text, TecdocAdmin)



admin.site.register(CarSection, TecdocAdmin)
