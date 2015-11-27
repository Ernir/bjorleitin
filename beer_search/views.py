from beer_search.forms import SearchForm
from beer_search.models import Beer, Style, ContainerType, GiftBox, \
    BeerType, BeerCategory
from beer_search.utils import perform_filtering, get_update_date, \
    num_per_style, num_per_store
from django.db.models import Q
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
    return render(request, "index.html", {
        "form": SearchForm(),
    })


def index_table(request):
    """

    Returns a rather raw HTML table of all available beers.
    Called via AJAX on the index page.
    """
    beers = Beer.objects.get_common_related()

    return render(request, "small_table.html", {
        "beers": beers,
    })


def overview(request):
    """

    A page consisting mostly of a single large table of all beers.
    """

    beers = Beer.objects.get_common_related()
    boxes = GiftBox.objects.get_common_related()
    title = "yfirlit allra bjóra"
    debug = settings.DEBUG
    explanation = "Hér má sjá alla bjóra sem til eru í " \
                  "Vínbúðinni á einni síðu."

    return render(request, "overview.html", {
        "beers": beers,
        "boxes": boxes,
        "debug": debug,
        "title": title,
        "explanation": explanation,
        "filtered": False
    })


def exciting(request):
    """

    As overview, above, but only shows new and/or temporary beers.
    """
    beers = Beer.objects.get_common_related().\
        filter(Q(new=True) | Q(temporary=True))

    boxes = GiftBox.objects.get_common_related().\
        filter(Q(new=True) | Q(temporary=True))

    title = "nýir og árstíðabundnir bjórar"
    debug = settings.DEBUG
    explanation = "Hér má sjá þá bjóra sem hafa verið í Vínbúðinni í " \
                  "innan við 60 daga eða eru í tímabundinni sölu."

    return render(request, "overview.html", {
        "beers": beers,
        "boxes": boxes,
        "debug": debug,
        "title": title,
        "explanation": explanation,
        "filtered": True
    })


def gift_boxes(request):
    """

    As overview, above, but only shows gift boxes rather than all products.
    """
    boxes = GiftBox.objects.get_common_related()
    title = "gjafaöskjur"
    debug = settings.DEBUG
    explanation = "Hér má sjá þá þær gjafaöskjur sem finna má í Vínbúðinni."

    return render(request, "overview.html", {
        "beers": [],
        "boxes": boxes,
        "debug": debug,
        "title": title,
        "explanation": explanation,
        "filtered": True
    })


def beers_in_category(request, category_slug):
    """

    As overview, above, but only shows beers belonging to the given cat.
    """

    category = BeerCategory.objects.get(url=category_slug)

    beer_types = category.beers.values("id")

    beers = Beer.objects.get_common_related().filter(
        beer_type_id__in=beer_types
    )

    boxes = category.boxes.select_related("country").all()

    title = category.name
    debug = settings.DEBUG
    explanation = category.description

    return render(request, "overview.html", {
        "beers": beers,
        "boxes": boxes,
        "debug": debug,
        "title": title,
        "explanation": explanation,
        "filtered": True
    })


def about(request):
    title = "um Bjórleitina"
    updated_at = get_update_date()

    return render(request, "about.html", {
        "title": title,
        "updated_at": updated_at
    })


def api_doc(request):
    title = "API"
    return render(request, "api_doc.html", {"title": title})


def statistics(request):
    """

    Displays various interesting statistics to show..
    """
    title = "Tölfræði"
    return render(request, "stats.html", {"title": title})


"""
Views used to deliver private or public API endpoints
"""


def get_beers_main_form(request):
    """

    Generates a list of beers to display based on request parameters.
    Returns their names and slugs in JSON format.
    As the name indicates, used to filter beers on the index page.
    """

    filtering_dict = {}
    if request.method == "POST":
        filtering_dict = request.POST
    elif request.method == "GET":
        filtering_dict = request.GET
    # Beer list
    bl = Beer.objects.filter(available=True).prefetch_related(
        "container", "beer_type", "beer_type__style",
        "beer_type__country")
    bl = perform_filtering(bl, filtering_dict)

    return_list = []
    for beer in bl.all():
        return_list.append({
            "name": beer.name,
            "suffix": beer.suffix,
            "atvr_id": beer.atvr_id
        })

    return JsonResponse(return_list, safe=False)


def get_distinct_properties(request, prop):
    """

    Accepts a standard Django request object, and the name of
    one property (prop) from the following list:

    ["name", "price", "abv", "volume"]

    And returns all unique values stored for that property, in JSON format.
    """

    assert prop in ["name", "price", "abv", "volume"], "Invalid property"

    if prop == "abv":
        objects = BeerType.objects.values(prop)
    else:
        objects = Beer.objects.available_beers().values(prop)

    return_dict = {}
    numbers = []
    for dictionary in objects:
        number = dictionary[prop]
        if number not in numbers:
            numbers.append(number)
    numbers.sort()
    return_dict["values"] = numbers

    return JsonResponse(return_dict)


def get_beers(request):
    """

    Public API view.
    Generates a list of beers to display based on GET parameters.
    Returns their JSON representation as defined by get_as_dict method
    in the Beer class.
    """

    if request.method == "GET":
        beer_queryset = Beer.objects.filter(
            available=True).prefetch_related("container", "beer_type",
                                             "beer_type__style",
                                             "beer_type__country")

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


def style_numbers(request):
    """
    Returns the number of beers associated with each individual style,
    as a JSON object with the style names as keys and the numbers as vals.
    """

    counts = num_per_style()
    return JsonResponse(counts)


def store_numbers(request):
    """
    Returns the number of beers available in each individual store in JSON.
    The top level object contains region names as keys, and as values
    an object that has store names as keys and their beer count as a value.
    """

    counts = num_per_store()
    return JsonResponse(counts)