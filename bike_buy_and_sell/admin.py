from django.contrib import admin
from .models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name'
    )
    search_fields = (
        'id',
        'name'
    )


class BikeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'price',
        'description',
        'category',
        'user',
        'status'
    )
    search_fields = (
        'id',
        'name',
        'price',
        'description',
        'category',
        'user',
        'status'
    )
    list_filter = ['status']


class BikeBuyAndSellImageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'bike_buy_and_sell',
        'image'
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(BikeBuyAndSell, BikeAdmin)
admin.site.register(BikeBuyAndSellImage, BikeBuyAndSellImageAdmin)


class OrdersAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'email',
        'address',
        'mobile',
        'total_price',
        'order_date',
        'status',
        'created_at'
    )
    search_fields = (
        'id',
        'user',
        'email',
        'address',
        'mobile',
        'total_price',
        'order_date',
        'status',
        'created_at'
    )
    list_filter = ['status']


admin.site.register(Orders, OrdersAdmin)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order',
        'bike_buy_and_sell',
        'created_at',
        'updated_at',
        'price',
        'quantity'
    )
    search_fields = (
        'id',
        'order',
        'bike_buy_and_sell',
        'created_at',
        'updated_at',
        'price',
        'quantity'
    )


admin.site.register(OrderItem, OrderItemAdmin)


class BannerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'banner_image'
    )


admin.site.register(Banner, BannerAdmin)
