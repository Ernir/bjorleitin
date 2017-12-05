from beer_search_v2.models import Product, ProductType, AlcoholCategory, SimplifiedStyle, UntappdStyle, UntappdEntity, \
    ContainerType, Brewery, Country, ModifiableSetting, RatebeerEntity, ProductList, ATVRProduct, JoGProduct
from django.contrib import admin


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ["name", "updated_at", "first_seen_at"]
    search_fields = ["name"]


class IsBeer(admin.SimpleListFilter):
    title = "er bjór"

    parameter_name = 'is-beer'

    def lookups(self, request, model_admin):
        return (
            ('true', 'Er Bjór'),
            ('false', 'Er Ekki Bjór'),
        )

    def queryset(self, request, queryset):
        beer = AlcoholCategory.objects.get(name="beer")
        if self.value() == 'true':
            return queryset.filter(alcohol_category=beer)
        if self.value() == 'false':
            return queryset.exclude(alcohol_category=beer)


class UntappdDefined(admin.SimpleListFilter):
    title = "Untappd skilgreint"

    parameter_name = 'untappd-defined'

    def lookups(self, request, model_admin):
        return (
            ('true', 'Skilgreint'),
            ('false', 'Óskilgreint'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'true':
            return queryset.filter(untappd_info__isnull=False)
        if self.value() == 'false':
            return queryset.filter(untappd_info__isnull=True)


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    search_fields = ["alias"]
    list_filter = (UntappdDefined, IsBeer)


@admin.register(SimplifiedStyle)
class SimplifiedStyleAdmin(admin.ModelAdmin):
    exclude = ["slug", "html_description"]


@admin.register(UntappdEntity)
class UntappdEntityAdmin(admin.ModelAdmin):
    search_fields = ["untappd_name", "untappd_id"]
    readonly_fields = ["untappd_name"]


@admin.register(Brewery)
class BreweryAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(ProductList)
class ProductTypeListAdmin(admin.ModelAdmin):
    filter_horizontal = ["products"]


admin.site.register(AlcoholCategory)
admin.site.register(Country)
admin.site.register(RatebeerEntity)
admin.site.register(UntappdStyle)
admin.site.register(ContainerType)
admin.site.register(ModifiableSetting)
admin.site.register(ATVRProduct)
admin.site.register(JoGProduct)
