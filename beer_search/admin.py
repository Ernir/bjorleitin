from beer_search.models import Style, Beer, ContainerType, Country
from django.contrib import admin

admin.site.register(Style)
admin.site.register(ContainerType)
admin.site.register(Country)


class BeerAdmin(admin.ModelAdmin):
    exclude = ("updated_at", "suffix")


admin.site.register(Beer, BeerAdmin)