from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from orders.models import Order
from orders.forms import CouponForm
from products.models import Product, Variation, Color, Size
from .models import Cart, Coupon
from billing.models import BillingProfile
from addresses.models import Address
from addresses.forms import AddressForm, ShippingAddressForm
from accounts.forms import LoginForm, GuestForm
from accounts.models import GuestEmail
# Create your views here.

def cart_create(user=None):
	cart_obj = Cart.objects.create(user=None)
	print("New Cart created")
	return cart_obj

def cart_home(request):
	cart_obj, new_obj = Cart.objects.new_or_get(request) 
	# print(request.POST)
	# add into cart view
	# cart_id = request.session.get("cart_id", None)
	# qs = Cart.objects.filter(id=cart_id)
	# if qs.count() == 1:
	# 	print('Cart ID exists')
	# 	cart_obj = qs.first()
	# 	if request.user.is_authenticated and cart_obj.user is None:
	# 		cart_obj.user = request.user
	# 		cart_obj.save()
	# else:
	# 	cart_obj = Cart.objects.new(user=request.user)
	# 	request.session['cart_id'] = cart_obj.id 

	# add total 
	# products = cart_obj.products.all()
	# total = 0
	# for x in products:
	# 	total += x.price  
	# # print(total)
	# cart_obj.total = total
	# cart_obj.save()
	context = {
		"cart": cart_obj,
		"form": CouponForm
	}

	return render(request, "carts/home.html", context) 



def cart_update(request):
	product_id 	= request.POST.get('product_id')
	
	if product_id is not None:
		try:
			product_obj = Product.objects.get(id=product_id)
		except Product.DoesNotExist:
			# print("Product is gon?")
			return redirect("carts:home")
		cart_obj, new_obj = Cart.objects.new_or_get(request)
		if product_obj in cart_obj.products.all():
			cart_obj.products.remove(product_obj)
			added = False
		else:
			# print(product_obj.id)
			# print(cart_obj)
			cart_obj.products.add(product_obj.id)
			added = True
		request.session['cart_items'] = cart_obj.products.count()

		if request.is_ajax():
			print("Ajax call")
			json_data = {
				"added": added,
				"remove": not added,
				"cart_items_count": cart_obj.products.count()
			}
			return JsonResponse(json_data)
	return redirect("carts:home") 


def getShipping(request, order_obj, billing_profile):
	if order_obj is not None:
		# print(order_obj.id)
		# print(billing_profile)
		try:
			shipping_address = Address.objects.filter(
					billing_profile=billing_profile,
					address_type="shipping" 
				).first()

			shipping_address_data = {
				'name': str(shipping_address.first_name) + " " + str(shipping_address.last_name),
				'address':{
				'line1': shipping_address.address_line_1,
				'line2': shipping_address.address_line_2,
				'postal_code': shipping_address.postal_code,
				'city': shipping_address.city,
				'state': shipping_address.state,
				'country': shipping_address.country,
				},
			}
			return shipping_address_data
		except ObjectDoesNotExist:
			print("Not getting shipping address for stripe charge!")


def checkout_home(request):
	cart_obj, cart_created = Cart.objects.new_or_get(request) 
	if cart_created or cart_obj.products.count() == 0:
		return redirect("carts:home")  
	
	user = request.user
	billing_profile = None
	login_form = LoginForm()
	guest_form = GuestForm()
	address_form = AddressForm()
	shipping_form = ShippingAddressForm()
	billing_address_id = request.session.get("billing_address_id", None)
	shipping_address_id = request.session.get("shipping_address_id", None)

	billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

	order_obj = None
	address_qs = None
	if billing_profile is not None:
		if request.user.is_authenticated:
			address_qs = Address.objects.filter(billing_profile=billing_profile)

		order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
		if shipping_address_id:
			order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
			del request.session["shipping_address_id"]
		if billing_address_id:
			order_obj.billing_address = Address.objects.get(id=billing_address_id)
			del request.session["billing_address_id"]
		if shipping_address_id or billing_address_id:
			order_obj.save() 


	if request.method == "POST":
		"check that order is done."
		is_done = order_obj.check_done()
		if is_done:
			#pass shipping address to strip mandotory
			shipping_address_data = getShipping(request, order_obj, billing_profile)
			# print(shipping_address_data)
			if shipping_address_data is not None:
				# call stripe charge method
				did_charge, charge_msg = billing_profile.charge(order_obj, shipping_address_data)
				if did_charge:
					order_obj.mark_paid()
					request.session['cart_items'] = 0
					del request.session['cart_id']
					return redirect("carts:success")
				else:
					print(charge_msg)
					return redirect("carts:checkout")
			# add custome error mdjango message
			return redirect("carts:checkout")

	context = {
		"object": order_obj,
		"billing_profile": billing_profile,
		"login_form": login_form,
		"guest_form": guest_form,
		"address_form": address_form,
		"shipping_form": shipping_form,
		"address_qs": address_qs

	}
	return render(request, "carts/checkout.html", context)

# Apply coupon code
def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "This coupon does not exist")
        return redirect("carts:checkout")

def add_coupon_view(request):
	coupon_code 	= request.POST.get('coupon_code') 
	print(coupon_code)
	if coupon_code is not None:
		try:
			coupon_obj = get_coupon(request, coupon_code)
			cart_obj, cart_created = Cart.objects.new_or_get(request)
			cart_obj.coupon = coupon_obj
			cart_obj.save()
			print("coupon_code apply")
			return redirect("carts:checkout")
		except ObjectDoesNotExist:
			print("coupon_code not apply")
			messages.info(self.request, "You do not have an active order")
			return redirect("carts:checkout")

	return redirect("carts:checkout")





def checkout_done_view(request):
	context = {}
	return render(request, "carts/checkout-done.html", context)


def add_to_cart_single_quantity(request, slug):
	if slug is not None:
		try:
			product_obj = Product.objects.get(slug=slug)
		except Product.DoesNotExist:
			print("Product is gon?")
			return redirect("carts:home")
		cart_obj, new_obj = Cart.objects.new_or_get(request)
		if cart_obj.quantity >= 0:
			cart_obj.quantity += 1
			cart_obj.save()

	return redirect("carts:home") 




def remove_from_cart_single_quantity(request, slug):
	if slug is not None:
		try:
			product_obj = Product.objects.get(slug=slug)
		except Product.DoesNotExist:
			print("Product is gon?")
			return redirect("carts:home")
		cart_obj, new_obj = Cart.objects.new_or_get(request)
		if cart_obj.quantity >= 1:
			cart_obj.quantity -= 1
			cart_obj.save()

	return redirect("carts:home")