from django.contrib import admin

from basketapp.models import Basket

# admin.site.register(Basket)

@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'total_price', 'quantity')
    list_filter = ('product',)

    def total_price(self, obj):
        return obj.product.price * obj.quantity