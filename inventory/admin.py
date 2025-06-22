from django.contrib import admin

from .models import Product, StockEntry, StockExit, StockAdjustment

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

@admin.register(StockEntry)
class StockEntryAdmin(admin.ModelAdmin):
    list_display = [
        'product',
        'quantity',
        'entry_date',
        'reason',
        'performed_by',
    ]
    list_filter = ['entry_date']
    search_fields = ['product__name', 'performed_by']
    ordering = ['-entry_date']

@admin.register(StockExit)
class StockExitAdmin(admin.ModelAdmin):
    list_display = [
        'product',
        'quantity',
        'exit_date',
        'reason',
        'performed_by',
    ]
    list_filter = ['exit_date']
    search_fields = ['product__name', 'performed_by']
    ordering = ['-exit_date']

@admin.register(StockAdjustment)
class StockAdjustmentAdmin(admin.ModelAdmin):
    list_display = [
        'product',
        'before',
        'after',
        'adjustment_date',
        'reason',
        'performed_by',
    ]
    list_filter = ['adjustment_date']
    search_fields = ['product__name', 'performed_by']
    ordering = ['-adjustment_date']

