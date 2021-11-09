from django.contrib import admin
from .models import *


class ProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Product._meta.fields]

    class Meta:
        model = Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Categories._meta.fields]

    class Meta:
        model = Categories


class ProductInBasketAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductInBasket._meta.fields]


    class Meta:
        model = ProductInBasket

class ProductInOrderInline(admin.TabularInline):
    model = ProductInOrder


class OrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Order._meta.fields]
    inlines = [ProductInOrderInline]

    class Meta:
        model = Order


admin.site.register(Product, ProductAdmin)
admin.site.register(Categories, CategoryAdmin)
admin.site.register(ProductInBasket, ProductInBasketAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(ProductInOrder  )
