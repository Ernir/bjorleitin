from beer_search.models import Style, Beer, ContainerType, Country, Region, \
    Store, BeerType, ModifiableSettings, GiftBox, Brewery, BeerCategory, UntappdStyle, \
    SimplifiedStyle
from django.contrib import admin


@admin.register(Beer)
class BeerAdmin(admin.ModelAdmin):
    exclude = ("updated_at", "suffix")
    search_fields = ["name"]


@admin.register(BeerType)
class BeerTypeAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(SimplifiedStyle)
class SimplifiedStyleAdmin(admin.ModelAdmin):
    exclude = ("slug", "html_description")


@admin.register(BeerCategory)
class BeerCategoryAdmin(admin.ModelAdmin):
    filter_horizontal = ("beers", "boxes")


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    filter_horizontal = ("beers_available", )


admin.site.register(Style)
admin.site.register(UntappdStyle)
admin.site.register(ContainerType)
admin.site.register(Country)
admin.site.register(Brewery)
admin.site.register(GiftBox)
admin.site.register(Region)
admin.site.register(ModifiableSettings)
