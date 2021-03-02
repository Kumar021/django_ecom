from django.urls import path
from . import views 

from .views import (
        cart_home,
        cart_update,
        checkout_home,
        checkout_done_view,
        add_to_cart_single_quantity,
        remove_from_cart_single_quantity,
        add_coupon_view,

)

app_name = 'carts'

urlpatterns = [
    
   	path('', cart_home, name='home'),
   	path('update/', cart_update, name='update'),
   	path('checkout/', checkout_home, name='checkout'),
    path('coupon/', add_coupon_view, name='coupon'),
    path('checkout/success/', checkout_done_view, name='success'),
    path('add-to-cart/<slug:slug>/', add_to_cart_single_quantity, name='add-to-cart'),
    path('remove-from-cart/<slug:slug>/', remove_from_cart_single_quantity, name='remove-from-cart'),
]