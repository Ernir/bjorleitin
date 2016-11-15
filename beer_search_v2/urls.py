from beer_search_v2 import views
from beer_search_v2.serializers import router
from django.conf.urls import url, include

urlpatterns = [
    url(r"^$", views.IndexView.as_view(), name="index"),
    url(r"^bjorstilar/$", views.StyleOverview.as_view(), name="styles"),
    url(r"^main-table/$", views.MainTableView.as_view(), name="main_table"),
    url(r"^main-table/(?P<format>.+)/$", views.MainTableView.as_view(), name="main_table_option"),
    url(r"^vara/(?P<pid>\d+)/$", views.SingleProductView.as_view(), name="single_product"),
    url(r"^listi/(?P<slug>.+)/$", views.ProductListView.as_view(), name="list_product"),
    url(r"^um/$", views.AboutView.as_view(), name="about"),
    url(r"^api/", include(router.urls))
]
