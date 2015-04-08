from beer_search.models import Beer
from django.shortcuts import render


def index(request):
    all_beers = Beer.objects.all()
    return render(request, "index.html", {"beers": all_beers})