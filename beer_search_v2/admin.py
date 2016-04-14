from beer_search_v2.models import Product, ProductType, AlcoholCategory, SimplifiedStyle, UntappdStyle, UntappdEntity, \
    ContainerType
from django.contrib import admin


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ["updated_at", "first_seen_at"]
    list_filter = ["source"]
    search_fields = ["name"]


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(SimplifiedStyle)
class SimplifiedStyleAdmin(admin.ModelAdmin):
    exclude = ["slug", "html_description"]


@admin.register(UntappdEntity)
class UntappdEntityAdmin(admin.ModelAdmin):
    search_fields = ["product_name", "untappd_id"]
    readonly_fields = ["product_name"]


admin.site.register(AlcoholCategory)
admin.site.register(UntappdStyle)
admin.site.register(ContainerType)
