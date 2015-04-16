from django.conf.urls import patterns, url
from beer_search import views

urlpatterns = \
    patterns('',
             url(r"^$", views.index, name="index"),
             url(r"^yfirlit/$", views.overview, name="overview"),

             url(r"^api/leit/$", views.perform_search, name="perform_search"),
             url(r"^api/gildi/(?P<eiginleiki>.+)/$", views.distinct_properties, name="distinct_properties")
    )