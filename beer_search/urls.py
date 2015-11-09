from django.conf.urls import patterns, url
from beer_search import views

urlpatterns = \
    patterns(
        '',

        # Actual pages
        url(r"^$", views.index, name="index"),
        url(r"^yfirlit/$", views.overview, name="overview"),
        url(r"^spennandi/$", views.exciting, name="exciting"),
        url(r"^gjafir/$", views.gift_boxes, name="gift_boxes"),
        url(r"^tolfraedi/$", views.statistics, name="statistics"),
        url(r"^um/$", views.about, name="about"),
        url(r"^api/$", views.api_doc, name="api-doc"),

        # API endpoints used internally
        url(r"^api/beers-minimal/$", views.get_beers_main_form,
            name="get_beers_main_form"),
        url(r"^api/distinct-values/(?P<prop>.+)/$",
            views.get_distinct_properties,
            name="get_distinct_properties"),

        url(r"^api/statistics/style-numbers/$", views.style_numbers,
            name="style_numbers"),
        url(r"^api/statistics/store-numbers/$", views.store_numbers,
            name="store_numbers"),
        
        # Public endpoints
        url(r"^api/beers/", views.get_beers, name="all_beers"),
        url(r"^api/styles/", views.get_styles, name="all_styles"),
        url(r"^api/containers/", views.get_containers,
            name="all_containers"),

        # No idea what to call something like this.
        # TODO Clean up the names.
        url(r"^small-table/$", views.index_table, name="index_table")
    )