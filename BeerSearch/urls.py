from django.conf.urls import include, url
from django.contrib import admin

from beer_search_v2 import views

urlpatterns = [
    url(r"^$", views.GoodByeView.as_view(), name="goodbye"),
    #    url(r'^', include("beer_search_v2.urls")),
    #    url(r'^admin/', include(admin.site.urls)),
    #    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
