from django.conf.urls import url
from cart import views

app_name = 'cart'
urlpatterns = [
            url(r'^$', views.show_cart, name='show_cart'),
            url(r'^add_to_cart/$', views.ajax_add_to_cart,
                name='add_to_cart'),
            url(r'^cart_update/$', views.ajax_cart_update,
                name='cart_update'),
]
