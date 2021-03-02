import random
import os
from django.db.models.signals import pre_save, post_save
from django.db.models import Q
from django.db import models
from django.urls import reverse
from ecom.utils import unique_slug_generator

CATEGORY_CHOICES = (
    ('S', 'Shirt'),
    ('SW', 'Sport wear'),
    ('OW', 'Outwear')
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)


def get_filename_ext(filepath):
	base_name 	= os.path.basename(filepath)
	name, ext 	= os.path.splitext(base_name)
	return name, ext 

def upload_image_path(instance, filename):
	# print(instance)
	# print(filename)
	new_filename = random.randint(1, 466565634020)
	name, ext = get_filename_ext(filename)
	final_filename = '{filename}{new_filename}{ext}'.format(filename=filename, new_filename=new_filename, ext=ext)
	return "products/{new_filename}/{final_filename}".format(new_filename=new_filename, final_filename=final_filename)



class Size(models.Model):
	name  	= models.CharField(max_length=120)
	
	def __str__(self):
		return self.name	

class Color(models.Model):
	name  	= models.CharField(max_length=120)
	
	def __str__(self):
		return self.name	
# variation 5
#  images
#	size
# 	color
#	price 
#	

class Variation(models.Model):
	color = models.ForeignKey(Color, null=True, blank=True, on_delete=models.CASCADE)
	size  = models.ForeignKey(Size, null=True, blank=True, on_delete=models.CASCADE)
	image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
	price = models.DecimalField(decimal_places=2, max_digits=10, default=0.00) 


	def __str__(self):
		return str(self.id)



# Create your models here.
class ProductQuerySet(models.QuerySet):
	def active(self):
		return self.filter(active=True)
	def featured(self):
		return self.filter(featured=True, active=True)

	def search(self, query):
		lookups = 	(Q(title__icontains=query) | 
					Q(description__icontains=query)|
					Q(tag__title__icontains=query)
					)	
		return self.filter(lookups).distinct()


class ProductManager(models.Manager):
	def get_queryset(self):
		return ProductQuerySet(self.model, using=self._db) 

	def all(self):
		return self.get_queryset().active()

	def featured(self): #Product.objects.featured()
		return self.get_queryset().featured()
 
	def get_by_id(self, id): 
		qs = self.get_queryset().filter(id=id)
		if qs.count() == 1:
			return qs.first()
		return None
	def search(self, query):
		lookups = Q(title__icontains=query) | Q(description__icontains=query)
		      #Q(tag__name__icontains=query) 
		      # t-shirt t shirt tshirt
		return self.get_queryset().active().search(query)



class Product(models.Model):
	title			= models.CharField(max_length=120)
	slug			= models.SlugField(blank=True, unique=True)
	category 		= models.CharField(choices=CATEGORY_CHOICES, max_length=2, blank=True, null=True)
	description		= models.TextField()
	price			= models.DecimalField(decimal_places=2, max_digits=10, default=0.00) 
	discount_price 	= models.FloatField(blank=True, null=True)
	image			= models.ImageField(upload_to=upload_image_path, null=True, blank=True)
	size			= models.ManyToManyField(Size, blank=True)
	color			= models.ManyToManyField(Color, blank=True)
	featured 		= models.BooleanField(default=False)
	active 			= models.BooleanField(default=True)


	objects = ProductManager()

	def get_absolute_url(self):
		#return "{slug}/".format(slug=self.slug)
		return reverse("products:detail", kwargs={"slug": self.slug})

	def __str__(self):
		return self.title 


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver, sender=Product) 
