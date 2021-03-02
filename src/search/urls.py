from django.urls import path
from . import views 

from .views import (
	SearchListView

)

app_name = 'search'

urlpatterns = [

   	path('product/', SearchListView.as_view(), name='query'),
]