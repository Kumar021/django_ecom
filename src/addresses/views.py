from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.core.exceptions import ObjectDoesNotExist
from billing.models import BillingProfile
from .models import Address
from .forms import AddressForm, ShippingAddressForm
from datetime import datetime, timedelta 


# billing address
def checkout_address_create_view(request):
	form = AddressForm(request.POST or None)
	context = {
        "form": form
    }
	next_ = request.GET.get('next')
	next_post = request.POST.get('next')
	redirect_path = next_ or next_post or None
	# print("request_path",redirect_path)
	# print("post",request.POST)
	if form.is_valid():
		print(request.POST)
		instance = form.save(commit=False)
		billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

		if billing_profile is not None:
			address_type = request.POST.get('address_type', 'billing')
			instance.billing_profile = billing_profile
			instance.address_type = address_type
			instance.save()

			request.session[address_type + "_address_id"] = instance.id
			print(address_type + "_address_id")
		else:
			print("Some error")
			return redirect("carts:checkout")

		if is_safe_url(redirect_path, request.get_host()):
			return redirect(redirect_path)

	return redirect("carts:checkout")


# shipping address
def checkout_shipping_address_create_view(request):
	form = ShippingAddressForm(request.POST or None)
	context = {
        "form": form
    }
	next_ = request.GET.get('next')
	next_post = request.POST.get('next')
	redirect_path = next_ or next_post or None
	# print("request_path",redirect_path)
	# print("post",request.POST)
	if form.is_valid():
		# print(request.POST)
		instance = form.save(commit=False)
		billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

		if billing_profile is not None:
			address_type = request.POST.get('address_type', 'shipping')
			instance.billing_profile = billing_profile
			instance.address_type = address_type
			instance.save()

			request.session[address_type + "_address_id"] = instance.id
			print(address_type + "_address_id")
		else:
			print("Some error")
			return redirect("carts:checkout")

		if is_safe_url(redirect_path, request.get_host()):
			return redirect(redirect_path)

	return redirect("carts:checkout")




# update shipping Address
def checkout_shipping_address_update_view(request):
	form = ShippingAddressForm(request.POST or None)
	print(request.POST)
	context = {
        "form": form
    }
	next_ = request.GET.get('next')
	next_post = request.POST.get('next')
	redirect_path = next_ or next_post or None
	# print("request_path",redirect_path)
	# print("post",request.POST)
	address_id = request.POST.get('address_id')
	address_line_1 = request.POST.get('address_line_1')
	address_line_2 = request.POST.get('address_line_2')
	city = request.POST.get('city')
	state = request.POST.get('state')
	country = request.POST.get('country')
	address_type = 'shipping'
	

	address_obj = Address.objects.filter(id=address_id).update(
			address_type=address_type,
			address_line_1=address_line_1,
			address_line_2=address_line_2,
			city=city,
			state=state,
			country=country
		)


	if is_safe_url(redirect_path, request.get_host()):
		return redirect(redirect_path)

	return redirect("carts:checkout")


def checkout_address_reuse_view(request):
	if request.user.is_authenticated:
		context = {}
		next_ = request.GET.get('next')
		next_post = request.POST.get('next')
		redirect_path = next_ or next_post or None

		if request.method == "POST":
			print(request.POST)
			shipping_address = request.POST.get('shipping_address', None)
			address_type = request.POST.get('address_type', 'shipping')
			billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
			if shipping_address is not None:
				qs = Address.objects.filter(billing_profile=billing_profile, id=shipping_address)
				if qs.exists():
					request.session[address_type + "_address_id"] = shipping_address

				if is_safe_url(redirect_path, request.get_host()):
					return redirect(redirect_path)

	return redirect("carts:checkout")











