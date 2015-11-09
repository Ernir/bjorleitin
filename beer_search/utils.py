from beer_search.models import Beer, Style, Region, BeerType
from django.db.models import Max, Min, Q, Count


def get_update_date():
    return Beer.objects.aggregate(Min("updated_at"))["updated_at__min"]


def perform_filtering(beer_q, request_body):
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
                beer_q = beer_q.filter(beer_type__style__id__in=styles)
        if "containers" in request_body:
            containers = request_body.getlist("containers")
            if len(containers) > 0:
                beer_q = beer_q.filter(container__id__in=containers)

        # Numerical filtering, in order:
        # * minimum and maximum volume
        # * minimum and maximum price
        # * minimum and maximum abv
        # * minimum and maximum untappd ratings
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
                max_abv = BeerType.objects.aggregate(Max("abv"))[
                    "abv__max"]
            beer_q = beer_q.filter(beer_type__abv__lte=max_abv)
        if "min_abv" in request_body:
            min_abv = request_body["min_abv"]
            if not len(min_abv) > 0:
                min_abv = 0
            beer_q = beer_q.filter(beer_type__abv__gte=min_abv)

        if "max_untappd" in request_body:
            max_untappd = request_body["max_untappd"]
            if not len(max_untappd) > 0:
                max_untappd = 5
            beer_q = beer_q.filter(
                Q(beer_type__isnull=True)
                | Q(beer_type__untappd_rating__lte=max_untappd)
            )

        if "min_untappd" in request_body:
            min_untappd = request_body["min_untappd"]
            if not len(min_untappd) > 0:
                min_untappd = 0
            beer_q = beer_q.filter(
                Q(beer_type__isnull=True)
                | Q(beer_type__untappd_rating__gte=min_untappd)
            )

        # Filter for new and temporary beers.
        if "noteworthy" in request_body:
            properties = request_body.getlist("noteworthy")
            if "new" in properties and "temporary" in properties:
                beer_q = beer_q.filter(Q(new=True) | Q(temporary=True))
            else:
                if "new" in properties:
                    beer_q = beer_q.filter(new=True)
                if "temporary" in properties:
                    beer_q = beer_q.filter(temporary=True)

        # Filter by stores.
        if "stores" in request_body:
            stores = request_body.getlist("stores")
            beer_q = beer_q.filter(store__in=stores)

    return beer_q


def num_per_style():
    """

    :return: A dict with style names as keys and the number of beers of
    that style as values.
    """

    return_set = {}
    for style in Style.objects.all():
        count = 0
        for beer_type in style.beertype_set.all():
            count += len(beer_type.beer_set.filter(available=True).all())
        if count > 0:
            return_set[style.name] = count
    return return_set


def num_per_store():
    """

    :return: A dict with region names as keys, and as values
    a dict that has store names as keys and their beer count as a value.
    """

    regions = Region.objects.all()

    return_set = {}

    for region in regions:
        stores = {}
        for store in region.store_set.all():
            stores[store.location] = store.beers_available.count()
        return_set[region.name] = stores

    return return_set