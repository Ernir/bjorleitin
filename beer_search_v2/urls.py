from beer_search_v2 import views
from beer_search_v2.serializers import router
from django.conf.urls import url, include

urlpatterns = [
    url(r"^$", views.IndexView.as_view(), name="index"),
    url(r"^main-table/$", views.MainTableView.as_view(), name="main_table"),
    url(r"^main-table/(?P<format>.+)/$", views.MainTableView.as_view(), name="main_table_option"),
    url(r"^api/", include(router.urls))
]
