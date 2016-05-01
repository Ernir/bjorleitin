from django.http import HttpResponse

from django.shortcuts import render
from django.views.generic import View
from beer_search_v2.models import MainQueryResult
from beer_search_v2.utils import get_main_display
from django.conf import settings

class BaseView(View):
    """
    An "abstract view" to manage the elements all of the site's
    pages have in common
    """

    def __init__(self):
        super().__init__()
        self.params = {
            "title": "Bjórleitin",  # Default value
            "sub_title": "",
            "debug": settings.DEBUG
        }


class IndexView(BaseView):
    """
    A view for the site's index page
    """

    def get(self, request):
        return render(request, "index-v2.html", self.params)


class MainTableView(BaseView):
    """
    A view to render a complete table of all beer types
    """

    def get(self, request):
        if settings.DEBUG:
            self.params["product_list"] = get_main_display()
        else:
            self.params["product_list"] = MainQueryResult.objects.first().json_contents
        return render(request, "main-table.html", self.params)
