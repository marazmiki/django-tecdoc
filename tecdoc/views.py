# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.views.generic import DetailView, ListView
from django.shortcuts import get_object_or_404, render
from tecdoc.models import (Supplier, CarModel, CarType, Manufacturer, Part,
                           Group, RootSection, CarSection)


class SupplierListView(ListView):
    model = Supplier
    template_name = 'tecdoc/suppliers.html'


class SupplierDetailView(DetailView):
    model = Supplier
    template_name = 'tecdoc/supplier.html'


class PartDetailView(DetailView):
    model = Part
    template_name = 'tecdoc/part.html'


class ManufacturerListView(ListView):
    queryset = Manufacturer.objects.distinct()
    template_name = 'tecdoc/manufacturers.html'


class ManufacturerDetailView(DetailView):
    model = Manufacturer
    template_name = 'tecdoc/manufacturer.html'
    context_object_name = 'object'


class CarTypeDetailView(DetailView):
    model = CarType
    template_name = 'tecdoc/cartype.html'


class CarModelDetailView(DetailView):
    model = CarModel
    template_name = 'tecdoc/cartypes.html'


class GroupDetailView(DetailView):
    model = Group
    template_name = 'tecdoc/group.html'


def category_tree(request, pk=None):
    cat = get_object_or_404(CarSection, id=pk) if pk else RootSection()
    return render(request, 'tecdoc/categories.html', {'cat': cat})


def category_tree_by_type(request, pk, parent=None):
    types = CarType.objects.filter(model=type_id)
    return render(request, 'tecdoc/cartypes.html', {'types': types,
                             'model': parent}
                            )

