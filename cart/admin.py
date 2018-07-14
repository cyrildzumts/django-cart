from django.contrib import admin
from cart.models import Cart, CartItem, LineItem


# Register your models here.
admin.site.register(CartItem)
admin.site.register(Cart)
