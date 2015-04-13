from beer_search.models import Beer
from django.shortcuts import render
from BeerSearch.settings import DEBUG


def index(request):
    all_beers = Beer.objects.all()
    return render(request, "index.html", {"beers": all_beers})


def overview(request):
    all_beers = Beer.objects.all()

    return render(request, "overview.html", {"beers": all_beers, "debug": DEBUG})