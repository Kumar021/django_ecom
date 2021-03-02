from django.urls import path
from . import views 

# from .views import (

# )

app_name = 'pages'

urlpatterns = [
    #path('list/', HomeView.as_view(), name='home'),
    path('', views.index, name='index'), #
    path('blog/list/', views.blog_list, name='list'), #blog/list
    path('shop/', views.shop, name='shop'),
    path('email/', views.email, name='email')
]