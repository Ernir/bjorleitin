from beer_search.models import Style, Beer, ContainerType, Country, Region, \
    Store, BeerType, ModifiableSettings, GiftBox, Brewery, BeerCategory, UntappdStyle, \
    SimplifiedStyle
from django.contrib import admin


class BeerAdmin(admin.ModelAdmin):
    exclude = ("updated_at", "suffix")


class SimplifiedStyleAdmin(admin.ModelAdmin):
    exclude = ("slug", "html_description")

admin.site.register(Style)
admin.site.register(UntappdStyle)
admin.site.register(SimplifiedStyle)
admin.site.register(ContainerType)
admin.site.register(Country)
admin.site.register(Beer, BeerAdmin)
admin.site.register(Brewery)
admin.site.register(GiftBox)
admin.site.register(BeerType)
admin.site.register(BeerCategory)
admin.site.register(Region)
admin.site.register(Store)
admin.site.register(ModifiableSettings)