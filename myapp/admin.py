from django.contrib import admin
from .models import (MyUser,
                     Goods,
                     Purchase,
                     ReturnGoods)

class MyUserAdmin(admin.ModelAdmin):
    fields = ('username', 'wallet')
    list_display = ("id", 'username', 'wallet')

admin.site.register(MyUser, MyUserAdmin)


class GoodsAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'price', 'quantity')
    list_display = ("id", 'name', 'description', 'price', 'quantity')

admin.site.register(Goods, GoodsAdmin)


class PurchaseAdmin(admin.ModelAdmin):
    fields = ('product', 'client', 'purchase_quantity')
    list_display = ('id','product', 'client', 'purchase_quantity', 'created_at')

admin.site.register(Purchase, PurchaseAdmin)


class ReturnGoodsAdmin(admin.ModelAdmin):
    field = ('purchase')
    list_display = ('id', 'purchase')

admin.site.register(ReturnGoods, ReturnGoodsAdmin)