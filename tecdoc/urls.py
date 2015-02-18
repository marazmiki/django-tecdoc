# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.conf.urls import url, include
from tecdoc import views


manufacturer_urlpatterns = [
    url(r'^$', views.ManufacturerListView.as_view(),
        name='tecdoc-manufacturers'),
    url(r'^(?P<pk>\d+)/$', views.ManufacturerDetailView.as_view(),
        name='tecdoc-manufacturer'),
]


supplier_urlpatterns = [
    url(r'^suppliers/$', views.SupplierListView.as_view(),
        name='suppliers'),
    url(r'^suppliers/(?P<pk>\d+)/$', views.SupplierDetailView.as_view(),
        name='supplier'),
]


cartype_urlpatterns = [
    url(r'^(?P<pk>\d+)/$', views.CarTypeDetailView.as_view(),
        name='car_type'),
    url(r'^(?P<pk>\d+)/category/$', views.category_tree_by_type,
        name='caregory_tree_by_type'),
    url(r'^(?P<pk>\d+)/category/(?P<parent>\d+)$', views.category_tree_by_type,
        name='caregory_tree_by_type'),
]

urlpatterns = [
    url(r'^manufacturers/', include(manufacturer_urlpatterns)),
    url(r'^suppliers/', include(supplier_urlpatterns)),
    url(r'^cartypes/', include(cartype_urlpatterns)),

    url(r'^models/(?P<pk>\d+)/$', views.CarModelDetailView.as_view(),
        name='tecdoc-models'),

    url(r'^categories/$', views.category_tree,
        name='category_tree'),
    url(r'^categories/(?P<pk>\d+)/$$', views.category_tree,
        name='category_tree'),

    url(r'^groups/(?P<pk>\d+)/$', views.GroupDetailView.as_view(), name='group'),
    url(r'^parts/(?P<pk>\d+)/$', views.PartDetailView.as_view(), name='part'),
]
