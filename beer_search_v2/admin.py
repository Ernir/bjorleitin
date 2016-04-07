from beer_search_v2.models import Product, ProductType, AlcoholCategory
from django.contrib import admin


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ["updated_at"]
    search_fields = ["name"]


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    search_fields = ["name"]


admin.site.register(AlcoholCategory)
