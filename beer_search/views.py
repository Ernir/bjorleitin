from beer_search.forms import SearchForm
from beer_search.models import Beer
from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import render


def index(request):
    return render(request, "index.html", {"form": SearchForm()})


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
        bl = Beer.objects

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

        return_list = []
        for beer in bl.all():
            return_list.append({
                "name": beer.name,
                "suffix": beer.suffix,
                "atvr_id": beer.atvr_id
            })

        return JsonResponse(return_list, safe=False)