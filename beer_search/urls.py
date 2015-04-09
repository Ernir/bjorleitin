from django.conf.urls import patterns, url
from beer_search import views

urlpatterns = \
    patterns('',
             url(r"^$", views.index, name="index"),
             url(r"^yfirlit/$", views.overview, name="overview")
    )