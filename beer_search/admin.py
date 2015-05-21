from beer_search.models import Style, Beer, ContainerType, Country, Region, \
    Store
from django.contrib import admin

admin.site.register(Style)
admin.site.register(ContainerType)
admin.site.register(Country)


class BeerAdmin(admin.ModelAdmin):
    exclude = ("updated_at", "suffix")


admin.site.register(Beer, BeerAdmin)

admin.site.register(Region)
admin.site.register(Store)