from beer_search.models import Beer
from django.db.models import Max, Min


def get_update_date():
    return Beer.objects.aggregate(Min("updated_at"))["updated_at__min"]


def perform_filtering(beer_q, request_body):
    print(request_body)
    """

    :param beer_q: An un-evaluated query for Beer objects.
    :param request_body: A dict-like object of parameters by which beer_q
    should be filtered.
    :return: A filtered queryset.
    """

    # Filtering is performed in succession, on defined parameters only.
    # If the parameter count is zero, no filtering is performed.
    if len(request_body) > 0:

        # Case-insensitive substring check.
        if "beer_name" in request_body:
            name = request_body["beer_name"]
            if len(name) > 0:
                beer_q = beer_q.filter(name__icontains=name)

        # Membership check for styles and containers.
        if "styles" in request_body:
            styles = request_body.getlist("styles")
            if len(styles) > 0:
                beer_q = beer_q.filter(style__id__in=styles)
        if "containers" in request_body:
            containers = request_body.getlist("containers")
            if len(containers) > 0:
                beer_q = beer_q.filter(container__id__in=containers)

        # Numerical filtering, in order:
        # * minimum and maximum volume
        # * minimum and maximum price
        # * minimum and maximum abv
        if "min_volume" in request_body:
            min_volume = request_body["min_volume"]
            if not len(min_volume) > 0:
                min_volume = 0
            beer_q = beer_q.filter(volume__gte=min_volume)
        if "max_volume" in request_body:
            max_volume = request_body["max_volume"]
            if not len(max_volume) > 0:
                # Setting default in case an empty string is sent
                max_volume = Beer.objects.aggregate(Max("volume"))[
                    "volume__max"]
            beer_q = beer_q.filter(volume__lte=max_volume)

        if "min_price" in request_body:
            min_price = request_body["min_price"]
            if not len(min_price) > 0:
                min_price = 0
            beer_q = beer_q.filter(price__gte=min_price)
        if "max_price" in request_body:
            max_price = request_body["max_price"]
            if not len(max_price) > 0:
                # Setting default in case an empty string is sent
                max_price = Beer.objects.aggregate(Max("price"))[
                    "price__max"]
            beer_q = beer_q.filter(price__lte=max_price)

        if "max_abv" in request_body:
            max_abv = request_body["max_abv"]
            if not len(max_abv) > 0:
                # Setting default in case an empty string is sent
                max_abv = Beer.objects.aggregate(Max("abv"))[
                    "abv__max"]
            beer_q = beer_q.filter(abv__lte=max_abv)
        if "min_abv" in request_body:
            min_abv = request_body["min_abv"]
            if not len(min_abv) > 0:
                min_abv = 0
            beer_q = beer_q.filter(abv__gte=min_abv)

        if "noteworthy" in request_body:
            properties = request_body.getlist("noteworthy")
            if "new" in properties:
                beer_q = beer_q.filter(new=True)
            if "seasonal" in properties:
                beer_q = beer_q.filter(seasonal=True)

    return beer_q