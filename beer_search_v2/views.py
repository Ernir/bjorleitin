from django.db.models import Max, Min
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View
from beer_search_v2.models import MainQueryResult, Product, AlcoholCategory, ContainerType
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
        base_query = Product.objects.select_related(
                "product_type"
        ).filter(
                product_type__alcohol_category=AlcoholCategory.objects.get(name="beer"),
                available=True
        ).exclude(
                container=ContainerType.objects.get(name="Gjafaaskja")
        ).exclude(
                container=ContainerType.objects.get(name="Kútur")
        )

        self.params["extremes"] = base_query.aggregate(
                min_abv=Min("product_type__abv"),
                max_abv=Max("product_type__abv"),
                min_price=Min("price"),
                max_price=Max("price")
        )
        return render(request, "index-v2.html", self.params)


class MainTableView(BaseView):
    """
    A view to render a complete table of all beer types
    """

    def get(self, request, format="html"):
        if settings.DEBUG:
            self.params["product_list"] = get_main_display()
        else:
            self.params["product_list"] = MainQueryResult.objects.first().json_contents

        if format == "html":
            return render(request, "main-table.html", self.params)
        elif format == "json":
            return JsonResponse({"beers": self.params["product_list"]})
