from django.urls import path
from . import views 

from .views import (
	ProductListView,
	#ProductDetailtView,
	ProductSlugDetailtView,
	#ProductFeaturedListView,
	#ProductFeaturedDetailtView,

)

app_name = 'products'

urlpatterns = [
    
    #path('featured/', ProductFeaturedListView.as_view(), name='featured-list'),
    #path('featured/<int:pk>/', ProductFeaturedDetailtView.as_view(), name='featured-detail'),
    #path('detail-c/<int:pk>/', ProductDetailtView.as_view(), name='detail'),
    #path('list/', views.product_list_view, name='product-list'), #fucntion view
    #path('detail/<int:pk>/', views.product_detail_view, name='product-detail'), #fucntion view
   	path('', ProductListView.as_view(), name='list'),
   	path('<slug:slug>/', ProductSlugDetailtView.as_view(), name='detail'),
]