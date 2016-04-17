from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from beer_search_v2.utils import get_product_type_display


class BaseView(View):
    """
    An "abstract view" to manage the elements all of the site's
    pages have in common
    """

    def __init__(self):
        super().__init__()
        self.params = {
            "title": "Bjórleitin",  # Default value
            "sub_title": ""
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
        self.params["product_list"] = get_product_type_display
        return render(request, "main-table.html", self.params)
