from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save, post_save, m2m_changed

from products.models import Product, Color 

class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.DecimalField(decimal_places=2, max_digits=10, default=0.00) 

    def __str__(self):
        return self.code


class CartManager(models.Manager):
	def new_or_get(self, request):
		cart_id = request.session.get("cart_id", None)
		qs = self.get_queryset().filter(id=cart_id, ordered=False)
		if qs.count() == 1:
			new_obj = False
			cart_obj = qs.first()
			if request.user.is_authenticated and cart_obj.user is None:
				cart_obj.user = request.user
				cart_obj.save()
		else:
			cart_obj = Cart.objects.new(user=request.user)
			new_obj = True
			request.session['cart_id'] = cart_obj.id
		return cart_obj, new_obj
	
	def new(self, user=None):
		user_obj = None
		if user is not None:
			if user.is_authenticated:
				user_obj = user
		return self.model.objects.create(user=user_obj)

class Cart(models.Model):
	user 		= models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
	products	= models.ManyToManyField(Product, blank=True)
	colors		= models.ManyToManyField(Color, blank=True)
	quantity 	= models.IntegerField(default=1)
	ordered 	= models.BooleanField(default=False)
	coupon 		= models.ForeignKey(Coupon, on_delete=models.SET_NULL, blank=True, null=True)
	total		= models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
	subtotal	= models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
	updated 	= models.DateTimeField(auto_now=True)
	timestamp 	= models.DateTimeField(auto_now_add=True)

	objects = CartManager()

	def __str__(self):
		return str(self.id)

	# def get_total_item_price(self):
	# 	return self.quantity * self.products.price 



	# total discount item price 
	# amout save 
	# final price


def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
	if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
		products = instance.products.all()
		total = 0
		for x in products:
			total += x.price 
		# print(total)
		if instance.coupon:
			total -= instance.coupon.amount
			print(total)

		if instance.subtotal != total:
			instance.subtotal = total
			instance.save() 

m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.products.through)


def pre_save_cart_receiver(sender, instance, *args, **kwargs):
	if instance.subtotal > 0:
		instance.total = float(instance.subtotal) * float(1.08) # add taxes and delivery charge
	else:
		instance.total = 0.00


pre_save.connect(pre_save_cart_receiver, sender=Cart)















