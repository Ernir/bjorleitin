from beer_search.models import Beer
from django.http import JsonResponse
from django.shortcuts import render
from BeerSearch.settings import DEBUG


def index(request):
    all_beers = Beer.objects.all()
    return render(request, "index.html", {"beers": all_beers})


def overview(request):
    all_beers = Beer.objects.all()
    title = "yfirlit allra bjóra"
    return render(request, "overview.html", {
        "beers": all_beers,
        "debug": DEBUG,
        "title": title,
    })


def perform_search(request):
    """
    Generates a list of beers to display based on POST parameters.
    Returns their names and slugs in JSON format.
    """
    if request.method == "GET":
        post_body = request.GET

        # Beer list
        bl = Beer.objects

        # Perform successive filtering based on POST contents.
        if len(post_body) > 0:
            if "beer_name" in post_body:
                name = post_body["beer_name"]
                if len(name) > 0:
                    bl = bl.filter(name__icontains=name)

        return_list = []
        for beer in bl.values(
                "name",
                "style__name",
                "container__name",
                "abv",
                "volume",
                "price",
                "atvr_id"
        ):
            return_list.append({
                "name": beer["name"],
                "style": beer["style__name"],
                "container": beer["container__name"],
                "abv": beer["abv"],
                "volume": beer["volume"],
                "price": beer["price"],
                "atvr_id": beer["atvr_id"]
            })

        return JsonResponse(return_list, safe=False)