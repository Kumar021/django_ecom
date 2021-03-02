from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from accounts.models import GuestEmail
from django.db.models.signals import pre_save, post_save, m2m_changed
 

import stripe 
stripe.api_key = "sk_test_hoYUDvffq9yzqVxdJ2DIAIpL00v6g5nTrF"

class BillingProfileManager(models.Manager):
    def new_or_get(self, request):
        user = request.user
        guest_email_id = request.session.get('new_guest_email')
        created = False
        obj = None
        if user.is_authenticated:
            'logged in user checkout; remember payment stuff'
            obj, created = self.model.objects.get_or_create(
                            user=user, email=user.email)
        elif guest_email_id is not None:
            'guest user checkout; auto reloads payment stuff'
            guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
            obj, created = self.model.objects.get_or_create(
                                            email=guest_email_obj.email)
        else:
            pass
        return obj, created


class BillingProfile(models.Model):
    user        = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    email       = models.EmailField()
    active      = models.BooleanField(default=True)
    update      = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    customer_id = models.CharField(max_length=120, null=True, blank=True) 

    objects = BillingProfileManager()
    
    def __str__(self):
        return self.email   

    def charge(self, order_obj, shipping_address_data, card=None):
        return Charge.objects.do(self, order_obj, shipping_address_data, card)    




def billing_profile_created_receiver(sender, instance, *args, **kwargs):
    if not instance.customer_id and instance.email:
        print("ACTUAL API REQUEST Send to stripe/braintree/razopay")
        customer = stripe.Customer.create(
                email = instance.email
            )
        # print(customer)
        instance.customer_id = customer.id

pre_save.connect(billing_profile_created_receiver, sender=BillingProfile)


def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)

post_save.connect(user_created_receiver, sender=User) 


class CardManager(models.Manager):
    def add_new(self, billing_profile, stripe_card_response):
        if str(stripe_card_response.object) == "card":
            new_card = self.model(
                    billing_profile=billing_profile,
                    stripe_id = stripe_card_response.id,
                    brand = stripe_card_response.brand,
                    country = stripe_card_response.country,
                    exp_month = stripe_card_response.exp_month,
                    exp_year = stripe_card_response.exp_year,
                    last4 = stripe_card_response.last4
                )
            new_card.save()
            return new_card
        return None


class Card(models.Model):
    billing_profile         = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    stripe_id               = models.CharField(max_length=120)
    brand                   = models.CharField(max_length=120, null=True, blank=True)
    country                 = models.CharField(max_length=20, null=True, blank=True)
    exp_month               = models.IntegerField(null=True, blank=True)
    exp_year                = models.IntegerField(null=True, blank=True)
    last4                   = models.CharField(max_length=4, null=True, blank=True)
    default                 = models.BooleanField(default=True)
    active                  = models.BooleanField(default=True)
    timestamp               = models.DateTimeField(auto_now_add=True) 

    objects = CardManager()

    def __str__(self):
        return "{} {}".format(self.brand, self.last4) 



def new_card_post_save_receiver(sender, instance, created, *args, **kwargs):
    if instance.default:
        billing_profile = instance.billing_profile
        qs = Card.objects.filter(billing_profile=billing_profile).exclude(pk=instance.pk)
        qs.update(default=False)


post_save.connect(new_card_post_save_receiver, sender=Card)



# stripe.Charge.create(
#   amount = int(order_obj.total * 100),
#   currency = "usd",
#   customer =  BillingProfile.objects.filter(email='hello@teamcfe.com').first().stripe_id,
#   source = Card.objects.filter(billing_profile__email='hello@teamcfe.com').first().stripe_id, # obtained with Stripe.js
#   description="Charge for elijah.martin@example.com"
# )

shipping={
        'name': 'Jenny Rosen',
        'address': {
          'line1': '510 Townsend St',
          'postal_code': '98140',
          'city': 'San Francisco',
          'state': 'CA',
          'country': 'US',
        },
      },

class ChargeManager(models.Manager):
    def do(self, billing_profile, order_obj, shipping_address_data, card=None): # Charge.objects.do()
        card_obj = card
        if card_obj is None:
            cards = billing_profile.card_set.filter(default=True) # card_obj.billing_profile
            if cards.exists():
                card_obj = cards.first()
        if card_obj is None:
            return False, "No cards available"
        c = stripe.Charge.create(
              amount = int(order_obj.total * 100), # 39.19 --> 3919
              currency = "usd",
              customer =  billing_profile.customer_id,
              source = card_obj.stripe_id,
              metadata={"order_id":order_obj.order_id},
              description='Ostryo services',
              shipping={
                'name': 'Jenny Rosen',
                'address': {
                  'line1': '510 Townsend St',
                  'postal_code': '98140',
                  'city': 'San Francisco',
                  'state': 'CA',
                  'country': 'US',
                },
              },
            )
        new_charge_obj = self.model(
                billing_profile = billing_profile,
                stripe_id = c.id,
                paid = c.paid,
                refunded = c.refunded,
                outcome = c.outcome,
                outcome_type = c.outcome['type'],
                seller_message = c.outcome.get('seller_message'),
                risk_level = c.outcome.get('risk_level'),
        )
        new_charge_obj.save()
        return new_charge_obj.paid, new_charge_obj.seller_message

class Charge(models.Model):
    billing_profile         = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    stripe_id               = models.CharField(max_length=120)
    paid                    = models.BooleanField(default=False)
    refunded                = models.BooleanField(default=False)
    outcome                 = models.TextField(null=True, blank=True)
    outcome_type            = models.CharField(max_length=120, null=True, blank=True)
    seller_message          = models.CharField(max_length=120, null=True, blank=True)
    risk_level              = models.CharField(max_length=120, null=True, blank=True)

    objects = ChargeManager() 

    def __str__(self):
        return str(self.stripe_id)






