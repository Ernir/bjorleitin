from beer_search.models import Style, Beer, ContainerType, Image
from django.contrib import admin

admin.site.register(Style)
admin.site.register(ContainerType)


class BeerAdmin(admin.ModelAdmin):
    exclude = ("updated_at", "suffix")


admin.site.register(Beer, BeerAdmin)