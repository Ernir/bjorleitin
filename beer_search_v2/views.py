from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max, Min, Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from beer_search_v2.models import Product, AlcoholCategory, ContainerType, SimplifiedStyle, \
    ProductType, UntappdEntity, ProductList
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
            "debug": settings.DEBUG,
            "product_lists": ProductList.objects.filter(visible=True).all()
        }


class IndexView(BaseView):
    """
    A view for the site's index page
    """

    def get(self, request):
        base_query = Product.objects.select_related(
                "product_type", "container", "product_type__alcohol_category"
        ).filter(
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

        first_visit = request.session.get("first_visit", True)
        if first_visit:
            request.session["first_visit"] = False
        self.params["show_welcome"] = first_visit

        return render(request, "index-v2.html", self.params)


class MainTableView(BaseView):
    """
    A view to render a complete table of all beer types
    """

    def get(self, request, format="html"):
        self.params["product_list"] = get_main_display()

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
            )

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
            self.params["similar_by_name"] = all_in_style.order_by("alias").all()
            self.params["similar_by_rating"] = all_in_style.order_by("-untappd_info__rating").all()

        self.params["title"] = product_type.alias
        self.params["product_type"] = product_type

        return render(request, "single-product.html", self.params)


class ProductListView(BaseView):
    def get(self, request, slug=None):

        try:
            if not slug:
                raise ObjectDoesNotExist
            the_list = ProductList.objects.get(slug=slug)
            products = the_list.products.prefetch_related(
                    "container",
                    "product_type",
                    "product_type__country"
            ).select_related(
                    "product_type__untappd_info",
                    "product_type__untappd_info__style",
                    "product_type__untappd_info__style__simplifies_to",
                    "product_type__untappd_info__brewery__country",
            ).all()
            self.params["product_list"] = products
            self.params["description"] = the_list.description
            self.params["title"] = the_list.name
        except ObjectDoesNotExist:
            self.params["product_list"] = []

        self.params["all_lists"] = ProductList.objects.filter(visible=True).all()

        return render(request, "product-list.html", self.params)


class AboutView(BaseView):
    """
    A view to show some information about the page.
    """

    def get(self, request):
        self.params["title"] = "Um Bjórleitina"
        return render(request, "about-v2.html", self.params)
