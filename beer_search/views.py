from beer_search.forms import SearchForm
from beer_search.models import Beer, Style, ContainerType
from beer_search.utils import perform_filtering, get_update_date
from django.db.models import Min
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.conf import settings


"""
Views defining individual pages
"""


def index(request):
    """

    The main page.
    """
    beers = Beer.objects.filter(available=True).all(). \
        prefetch_related("style", "container")

    updated_at = get_update_date()

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
    updated_at = get_update_date()

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


def api_doc(request):
    title = "API"
    return render(request, "api_doc.html", {"title": title})


"""
Views used to deliver private or public API endpoints
"""


def get_beers_main_form(request):
    """

    Generates a list of beers to display based on POST parameters.
    Returns their names and slugs in JSON format.
    As the name indicates, used to filter beers on the index page.
    """
    if request.method == "POST":
        # Beer list
        bl = Beer.objects.filter(available=True)
        bl = perform_filtering(bl, request.POST)

        return_list = []
        for beer in bl.all():
            return_list.append({
                "name": beer.name,
                "suffix": beer.suffix,
                "atvr_id": beer.atvr_id
            })

        return JsonResponse(return_list, safe=False)


def get_distinct_properties(request, eiginleiki):
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


def get_beers(request):
    """

    Public API view.
    Generates a list of beers to display based on GET parameters.
    Returns their JSON representation as defined by get_as_dict method
    in the Beer class.
    """

    if request.method == "GET":
        beer_queryset = Beer.objects.filter(available=True) \
            .prefetch_related("style", "container")

        beer_queryset = perform_filtering(beer_queryset, request.GET)

        return_dict = {"updated_at": get_update_date()}
        beers = [beer.get_as_dict() for beer in beer_queryset.all()]
        return_dict["beers"] = beers

        return JsonResponse(return_dict)
    else:
        return HttpResponse(status=405)


def get_styles(request):
    """

    Public API view.
    Returns a complete list of JSON-serialized Style objects.
    """
    if request.method == "GET":
        style_queryset = Style.objects

        return_dict = {}
        styles = [style.get_as_dict() for style in style_queryset.all()]
        return_dict["styles"] = styles

        return JsonResponse(return_dict)
    else:
        return HttpResponse(status=405)


def get_containers(request):
    """

    Public API view.
    Returns a complete list of JSON-serialized ContainerType objects.
    """
    if request.method == "GET":
        container_queryset = ContainerType.objects

        return_dict = {}
        containers = [co.get_as_dict() for co in container_queryset.all()]
        return_dict["containers"] = containers

        return JsonResponse(return_dict)
    else:
        return HttpResponse(status=405)