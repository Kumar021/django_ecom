
<!-- #view -->
<!-- from django.http import Http404
from django.views.generic import ListView,DetailView
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import Product 



class ProductFeaturedListView(ListView):
	#queryset = Product.objects.all() 
	template_name = "products/list.html" 

	def get_queryset(self, *args, **kwargs):
		request = self.request
		return Product.objects.all().featured()

class ProductFeaturedDetailtView(DetailView):
	queryset = Product.objects.all().featured() 
	template_name = "products/featured-detail.html" 

	# def get_queryset(self, *args, **kwargs):
	# 	request = self.request
	# 	return Product.objects.featured()

	


class ProductListView(ListView):
	#queryset = Product.objects.all() 
	template_name = "products/list.html" 

	# def get_context_data(self, *args, **kwargs):
	# 	context = super(ProductListView, self).get_context_data(*args, **kwargs)
	# 	print(context)
	# 	return context 

	def get_queryset(self, *args, **kwargs):
		request = self.request
		return Product.objects.all()

def product_list_view(request):
	queryset = Product.objects.all()
	context = {
		'object_list': queryset
	}
	return render(request, "products/list.html", context)


class ProductSlugDetailtView(DetailView):
	#queryset = Product.objects.all() 
	#print("data:", queryset)
	template_name = "products/detail.html" 

	# def get_absolute_url(self):
	# 	return reverse('detail-slug', kwargs={'slug': self.slug}) 

	def get_object(self, *args, **kwargs):
		request = self.request
		slug = self.kwargs.get('slug')
		qs = Product.objects.filter(slug=slug) #get_object_or_404(Product, slug=slug)
		if qs is None:
			raise Http404("Product not found.")
		return qs.first() 


class ProductDetailtView(DetailView):
	queryset = Product.objects.all() 
	template_name = "products/detail.html" 

	def get_context_data(self, *args, **kwargs):
		context = super(ProductDetailtView, self).get_context_data(*args, **kwargs)
		print(context)
		#context["abc"] = 123
		return context  

	def get_object(self, *args, **kwargs):
		request = self.request
		pk = self.kwargs.get('pk')
		instance = Product.objects.get_by_id(pk)
		if instance is None:
			raise Http404("Product not found.")
		return instance 

	# def get_queryset(self, *args, **kwargs):
	# 	request = self.request
	# 	pk = self.kwargs.get('pk')
	# 	return Product.objects.filter(pk=pk)


def product_detail_view(request, pk=None, *args, **kwargs):
	#instance = Product.objects.get(pk=pk) #is = pk
	#instance = get_object_or_404(Product, pk=pk)
	# try:
	# 	instance = Product.objects.get(id=pk)
	# except Product.DoesNotExist:
	# 	raise Http404("Product not found!!")
	# except:
	# 	print("Huu?") 

	instance = Product.objects.get_by_id(pk)
	if instance is None:
		raise Http404("Product not found!!")
	#print(instance)

	# qs = Product.objects.filter(id=pk)
	# if qs.exists() and qs.count() == 1:
	# 	instance = qs.first()
	# else:
	# 	raise Http404("Product not found!!")
	


	context = {
		'object': instance
	}
	return render(request, "products/detail.html", context)





# urls
app_name = 'products'

urlpatterns = [
    
    #path('featured/', ProductFeaturedListView.as_view(), name='featured-list'),
    #path('featured/<int:pk>/', ProductFeaturedDetailtView.as_view(), name='featured-detail'),
    #path('detail-c/<int:pk>/', ProductDetailtView.as_view(), name='detail'),
    #path('list/', views.product_list_view, name='product-list'), #fucntion view
    #path('detail/<int:pk>/', views.product_detail_view, name='product-detail'), #fucntion view
   	path('list/', ProductListView.as_view(), name='list'),
   	path('detail/<slug:slug>/', ProductSlugDetailtView.as_view(), name='detail'),
]













 -->