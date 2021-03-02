from django.db import models
from billing.models import BillingProfile



ADDRESS_TYPES = (
    ('billing', 'Billing address'),
    ('shipping', 'Shipping address'),
)


class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, null=True, blank=True, on_delete=models.CASCADE)
    first_name      = models.CharField(max_length=120, null=True, blank=True)
    last_name       = models.CharField(max_length=120, null=True, blank=True)
    email           = models.EmailField(max_length=120, null=True, blank=True)
    address_type    = models.CharField(max_length=120, choices=ADDRESS_TYPES)
    address_line_1  = models.CharField(max_length=120)
    address_line_2  = models.CharField(max_length=120, null=True, blank=True)
    city            = models.CharField(max_length=120)
    country         = models.CharField(max_length=120, default='India')
    state           = models.CharField(max_length=120)
    postal_code     = models.CharField(max_length=120)


    def __str__(self):
    	return str(self.id)


    def get_address(self):
        return "{email}\n{line1}\n{line2}\n{city}\n{state}\n{country}\n, {postal_code}".format(
                email=self.email,
                line1=self.address_line_1,
                line2=self.address_line_2 or "",
                city=self.city,
                state=self.state,
                country=self.country,
                postal_code=self.postal_code,
            )


