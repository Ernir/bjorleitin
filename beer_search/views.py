from beer_search.forms import SearchForm
from beer_search.models import Beer
from django.db.models import Max, Min
from django.http import JsonResponse
from django.shortcuts import render


def index(request):
    updated_at = Beer.objects.aggregate(
        Min("updated_at")
    )["updated_at__min"]
    return render(request, "index.html", {
        "form": SearchForm(),
        "updated_at": updated_at
    })


def overview(request):
    all_beers = Beer.objects.all()
    title = "yfirlit allra bjóra"
    debug = False  # ToDo: use config var instead
    return render(request, "overview.html", {
        "beers": all_beers,
        "debug": debug,
        "title": title,
    })


def perform_search(request):
    """
    Generates a list of beers to display based on POST parameters.
    Returns their names and slugs in JSON format.
    """
    if request.method == "POST":
        post_body = request.POST

        # Beer list
        bl = Beer.objects.filter(available=True)

        # Perform successive filtering based on POST contents.
        if len(post_body) > 0:
            if "beer_name" in post_body:
                name = post_body["beer_name"]
                if len(name) > 0:
                    bl = bl.filter(name__icontains=name)

            if "styles" in post_body:
                styles = post_body.getlist("styles")
                if len(styles) > 0:
                    bl = bl.filter(style__id__in=styles)

            if "containers" in post_body:
                containers = post_body.getlist("containers")
                if len(containers) > 0:
                    bl = bl.filter(container__id__in=containers)

            if "min_volume" in post_body:
                min_volume = post_body["min_volume"]
                if not len(min_volume) > 0:
                    min_volume = 0
                bl = bl.filter(volume__gte=min_volume)
            if "max_volume" in post_body:
                max_volume = post_body["max_volume"]
                if not len(max_volume) > 0:
                    # Setting default in case an empty string is sent
                    max_volume = Beer.objects.aggregate(Max("volume"))["volume__max"]
                bl = bl.filter(volume__lte=max_volume)

            if "min_price" in post_body:
                min_price = post_body["min_price"]
                if not len(min_price) > 0:
                    min_price = 0
                bl = bl.filter(price__gte=min_price)
            if "max_price" in post_body:
                max_price = post_body["max_price"]
                if not len(max_price) > 0:
                    # Setting default in case an empty string is sent
                    max_price = Beer.objects.aggregate(Max("price"))["price__max"]
                bl = bl.filter(price__lte=max_price)

            if "max_abv" in post_body:
                max_abv = post_body["max_abv"]
                if not len(max_abv) > 0:
                    # Setting default in case an empty string is sent
                    max_abv = Beer.objects.aggregate(Max("abv"))["abv__max"]
                bl = bl.filter(abv__lte=max_abv)
            if "min_abv" in post_body:
                min_abv = post_body["min_abv"]
                if not len(min_abv) > 0:
                    min_abv = 0
                bl = bl.filter(abv__gte=min_abv)

        return_list = []
        for beer in bl.all():
            return_list.append({
                "name": beer.name,
                "suffix": beer.suffix,
                "atvr_id": beer.atvr_id
            })

        return JsonResponse(return_list, safe=False)


def distinct_properties(request, eiginleiki):

    p = "name"  # p for property
    if eiginleiki == "rummal":
        p = "volume"
    elif eiginleiki == "verd":
        p = "price"

    objects = Beer.objects.filter(available=True).values(p)
    numbers = []
    for dictionary in objects:
        number = dictionary[p]
        if number not in numbers:
            numbers.append(number)
    numbers.sort()

    return JsonResponse(numbers, safe=False)