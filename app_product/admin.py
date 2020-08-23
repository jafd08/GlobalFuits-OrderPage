from django.contrib import admin

from django.contrib import admin

from .models import Category, Product, Measure

@admin.register(Measure)
class MeasureAdmin(admin.ModelAdmin):
    search_fields = ['title']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['title']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'tag_final_value','measure', 'qty', 'active']
    list_select_related = ['category']
    list_filter = ['active', 'category']
    search_fields = ['title']
    list_per_page = 50
    fields = ['active', 'title', 'category', 'qty', 'value', 'measure', 'tag_final_value']
    autocomplete_fields = ['category']
    readonly_fields = ['tag_final_value']
