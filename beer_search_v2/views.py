from django.db.models import Max, Min, Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from beer_search_v2.models import MainQueryResult, Product, AlcoholCategory, ContainerType, SimplifiedStyle, \
    ProductType, \
    UntappdEntity
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
            "title": "",
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
                Q(available_in_atvr=True) | Q(available_in_jog=True),
                product_type__alcohol_category=AlcoholCategory.objects.get(name="beer")
        ).exclude(
                container=ContainerType.objects.get(name="Gjafaaskja")
        ).exclude(
                container=ContainerType.objects.get(name="Kútur")
        )

        self.params["extremes"] = base_query.aggregate(
                min_abv=Min("product_type__abv"),
                max_abv=Max("product_type__abv"),
                min_price=Min("price"),
                max_price=Max("price"),
                min_volume=Min("volume"),
                max_volume=Max("volume")
        )
        self.params["styles"] = SimplifiedStyle.objects.all()
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


class StyleOverview(BaseView):
    """
    A view to display information about the simplified beer styles.
    """

    def get(self, request):
        self.params["title"] = "Upplýsingar um bjórstíla"
        self.params["styles"] = SimplifiedStyle.objects.all()
        return render(request, "style_info_v2.html", self.params)


class SingleProductView(BaseView):
    """
    A "detail" view to display information about a particular product type, including availability and recommendations.
    """

    def get(self, request, pid):
        product_type = get_object_or_404(ProductType, id=pid)

        # This is where we find beers which are similar to the
        all_in_style = []
        if product_type.untappd_info and product_type.untappd_info.style.simplifies_to:
            product_type.simple_style = product_type.untappd_info.style.simplifies_to
            all_in_style = ProductType.objects.filter(
                    untappd_info__style__simplifies_to=product_type.untappd_info.style.simplifies_to
            ).all()

            total_count = UntappdEntity.objects.count()
            lower_rated_count = UntappdEntity.objects.filter(rating__lt=product_type.untappd_info.rating).count()
            lower_rated_percentage = round(lower_rated_count / total_count * 100)

            ue_in_style = UntappdEntity.objects.filter(style__simplifies_to=product_type.simple_style)
            style_count = ue_in_style.count()
            style_lower_rated_count = ue_in_style.filter(rating__lt=product_type.untappd_info.rating).count()
            style_lower_rated_percentage = round(style_lower_rated_count / style_count * 100)

            self.params["total_count"] = total_count
            self.params["lower_rated_count"] = lower_rated_count
            self.params["lower_rated_percentage"] = lower_rated_percentage

            self.params["style_count"] = style_count
            self.params["style_lower_rated_count"] = style_lower_rated_count
            self.params["style_lower_rated_percentage"] = style_lower_rated_percentage

        self.params["title"] = product_type.alias
        self.params["product_type"] = product_type
        self.params["similar"] = all_in_style

        return render(request, "single-product.html", self.params)
