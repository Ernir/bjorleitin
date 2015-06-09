from beer_search.forms import SearchForm
from beer_search.models import Beer, Style, ContainerType
from beer_search.utils import perform_filtering, get_update_date, \
    num_lagers_and_ales, num_per_style
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
    beers = Beer.objects.filter(available=True).all(). \
        prefetch_related("style", "container", "country")

    return render(request, "small_table.html", {
        "beers": beers,
    })


def overview(request):
    """

    A page consisting mostly of a single large table of all beers.
    """

    beer_q = Beer.objects.all().\
        prefetch_related("style", "container", "country")
    title = "yfirlit allra bjóra"
    debug = settings.DEBUG
    explanation = "Hér má sjá alla bjóra sem til eru í " \
                  "Vínbúðinni á einni síðu."

    return render(request, "overview.html", {
        "beers": beer_q,
        "debug": debug,
        "title": title,
        "explanation": explanation,
        "filtered": False
    })


def exciting(request):
    """

    As overview, above, but only shows new and/or seasonal beers.
    """
    beer_q = Beer.objects.filter(Q(new=True) | Q(seasonal=True)) \
        .all().prefetch_related("style", "container")
    title = "nýir og árstíðabundnir bjórar"
    debug = settings.DEBUG
    explanation = "Hér má sjá þá bjóra sem eru tiltölulega nýir í " \
                  "Vínbúðinni og/eða árstíðabundnir."

    return render(request, "overview.html", {
        "beers": beer_q,
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

    Calculates various interesting statistics to show.
    Don't go here on an empty DB, it will cause zero divisions.
    """

    all_available = Beer.available_beers.prefetch_related("style")

    lager_ale_counts = num_lagers_and_ales()
    lager_ratio = int(lager_ale_counts["lagers"]/all_available.count()*100)

    return render(
        request,
        "stats.html", {
            "number": all_available.count(),

            "lager_ratio": lager_ratio
        }
    )


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


def get_distinct_properties(request, prop):
    """

    Accepts a standard Django request object, and the name of
    one property (prop) from the following list:

    ["name", "price", "abv"]

    And returns all unique values stored for that property, in JSON format.
    """

    objects = Beer.objects.filter(available=True).values(prop)

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


def style_numbers(request):
    """
    Returns the number of beers associated with each individual style,
    as a JSON object with the style names as keys and the numbers as vals.
    """

    counts = num_per_style()
    return JsonResponse(counts)