  
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static

from addresses.views import (checkout_address_create_view, 
                            checkout_shipping_address_create_view, 
                            checkout_address_reuse_view,
                            checkout_shipping_address_update_view
                        )
from billing.views import payment_method_view, payment_method_createview
from accounts.views import login_page, guest_register_page, register_page, logout_view 


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^login/$', login_page, name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^register/$', register_page, name='register'),
    url(r'^billing/payment/$', payment_method_view, name='billing-payment'),
    url(r'^billing/payment/create/$', payment_method_createview, name='billing-payment-create'),
    url(r'^register/guest/$', guest_register_page, name='guest_register'),
    url(r'^checkout/address/create/$', checkout_address_create_view, name='checkout_address_create'),
    url(r'^checkout/shpipping/address/update/$', checkout_shipping_address_update_view, name='checkout_shipping_address_update'),
    
    url(r'^checkout/shipping-address/create/$', checkout_shipping_address_create_view, name='checkout_shipping_address_create'),
    url(r'^checkout/address/reuse/$', checkout_address_reuse_view, name='checkout_address_reuse'),
    path('', include('pages.urls')),
    path('product/', include('products.urls', namespace='products')),
    path('cart/', include('carts.urls', namespace='carts')),
    path('search/', include('search.urls', namespace='search')),
]

if settings.DEBUG:
    # import debug_toolbar
    # urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
