from django.conf.urls import patterns, url
from beer_search import views

urlpatterns = \
    patterns('',
             url(r"^$", views.index, name="index"),
             url(r"^yfirlit/$", views.overview, name="overview"),
             url(r"^um/", views.about, name="about"),

             url(r"^api/$", views.api_doc, name="api-doc"),

             url(r"^api/leit/$", views.get_beers_main_form, name="get_beers_main_form"),
             url(r"^api/einstok-gildi/(?P<eiginleiki>.+)/$", views.get_distinct_properties, name="get_distinct_properties"),
             url(r"^api/beers/", views.get_beers, name="all_beers"),
             url(r"^api/styles/", views.get_styles, name="all_styles"),
             url(r"^api/containers/", views.get_containers, name="all_containers")
    )