from django import forms 

from .models import Address 

# billing address
class AddressForm(forms.ModelForm):
	class Meta:
		model = Address
		fields = [
            #'billing_profile',
            #'address_type',
            'address_line_1',
            'address_line_2',
            'city',
            'country',
            'state',
            'postal_code'
        ]

#shipping Adrress
class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            #'billing_profile',
            #'address_type',
            'first_name',
            'last_name',
            'email',
            'address_line_1',
            'address_line_2',
            'city',
            'country',
            'state',
            'postal_code'
        ]