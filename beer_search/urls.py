from django.conf.urls import patterns, url
from beer_search import views

urlpatterns = \
    patterns(
        '',

        # Actual pages
        url(r"^$", views.index, name="index"),
        url(r"^yfirlit/$", views.overview, name="overview"),
        url(r"^spennandi/$", views.exciting, name="exciting"),
        url(r"^um/$", views.about, name="about"),
        url(r"^api/$", views.api_doc, name="api-doc"),

        # API endpoints used internally
        url(r"^api/beers-minimal/$", views.get_beers_main_form,
            name="get_beers_main_form"),
        url(r"^api/distinct-values/(?P<prop>.+)/$",
            views.get_distinct_properties,
            name="get_distinct_properties"),
        
        # Public endpoints
        url(r"^api/beers/", views.get_beers, name="all_beers"),
        url(r"^api/styles/", views.get_styles, name="all_styles"),
        url(r"^api/containers/", views.get_containers,
            name="all_containers")

    )