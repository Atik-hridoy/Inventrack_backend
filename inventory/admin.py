from django.contrib import admin

from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'description',
        'price',
        'quantity',
        'image',
        'sku',
        'category',  
    ]
    list_filter = ['category',]
    search_fields = ['name', 'sku', 'category__name']
    ordering = ['name']
