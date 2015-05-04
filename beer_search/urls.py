from django.conf.urls import patterns, url
from beer_search import views

urlpatterns = \
    patterns('',
             url(r"^$", views.index, name="index"),
             url(r"^yfirlit/$", views.overview, name="overview"),
             url(r"^um/", views.about, name="about"),

             url(r"^api/leit/$", views.filter_beers_by_request_params, name="filter_beers_by_request_params"),
             url(r"^api/einstok-gildi/(?P<eiginleiki>.+)/$", views.distinct_properties, name="distinct_properties")
    )