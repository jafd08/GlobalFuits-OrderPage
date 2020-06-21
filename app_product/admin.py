from django.contrib import admin

from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['title']
8

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'tag_final_value','unidad_o_kg', 'qty', 'active']
    list_select_related = ['category']
    list_filter = ['active', 'category']
    search_fields = ['title']
    list_per_page = 50
    fields = ['active', 'title', 'category', 'qty', 'value', 'unidad_o_kg', 'tag_final_value']
    autocomplete_fields = ['category']
    readonly_fields = ['tag_final_value']
