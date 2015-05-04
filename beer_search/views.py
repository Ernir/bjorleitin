from beer_search.forms import SearchForm
from beer_search.models import Beer
from beer_search.utils import perform_filtering
from django.db.models import Min
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings


def index(request):
    """

    The main page.
    """
    beers = Beer.objects.filter(available=True).all(). \
        prefetch_related("style", "container")

    updated_at = Beer.objects. \
        aggregate(Min("updated_at"))["updated_at__min"]

    return render(request, "index.html", {
        "form": SearchForm(),
        "beers": beers,
        "updated_at": updated_at
    })


def overview(request):
    """

    A page consisting mostly of a single large table of all beers.
    """

    all_beers = Beer.objects.all().prefetch_related("style", "container")
    title = "yfirlit allra bjóra"
    debug = settings.DEBUG
    updated_at = Beer.objects. \
        aggregate(Min("updated_at"))["updated_at__min"]

    return render(request, "overview.html", {
        "beers": all_beers,
        "debug": debug,
        "title": title,
        "updated_at": updated_at
    })


def about(request):
    title = "um Bjórleitina"
    updated_at = Beer.objects. \
        aggregate(Min("updated_at"))["updated_at__min"]

    return render(request, "about.html", {
        "title": title,
        "updated_at": updated_at
    })


def filter_beers_by_request_params(request):
    """

    Generates a list of beers to display based on POST parameters.
    Returns their names and slugs in JSON format.
    """
    if request.method == "POST":
        post_body = request.POST

        # Beer list
        bl = Beer.objects.filter(available=True)

        bl = perform_filtering(bl, post_body)

        return_list = []
        for beer in bl.all():
            return_list.append({
                "name": beer.name,
                "suffix": beer.suffix,
                "atvr_id": beer.atvr_id
            })

        return JsonResponse(return_list, safe=False)


def distinct_properties(request, eiginleiki):
    """

    Accepts a standard Django request object, and the Icelandic name of
    one property from the following list:

    ["rummal", "verd", "prosenta"]

    And returns all unique value stored for that property, in JSON format.
    """
    p = "name"  # p for property
    if eiginleiki == "rummal":
        p = "volume"
    elif eiginleiki == "verd":
        p = "price"
    elif eiginleiki == "prosenta":
        p = "abv"

    objects = Beer.objects.filter(available=True).values(p)
    numbers = []
    for dictionary in objects:
        number = dictionary[p]
        if number not in numbers:
            numbers.append(number)
    numbers.sort()

    return JsonResponse(numbers, safe=False)