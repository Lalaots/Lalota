from django.contrib import admin
from .models import Product, Sale, SaleItem

@admin.register(Product)
class ProductClass(admin.ModelAdmin):
    list_display= ('name','price','stock_quantity')
    search_fields= ('Name',)

@admin.register(Sale)
class SaleClass(admin.ModelAdmin):
    list_display= ('id','date_time', 'subtotal', 'tax', 'total', 'payment','change')
    search_fields= ('ID',)

@admin.register(SaleItem)
class SaleItemClass(admin.ModelAdmin):
    list_display= ('sale','product','quantity','item_total')
    search_fields= ('Sale',)