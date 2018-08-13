from django.db import models
from django.conf import settings
# Create your models here.
# from django.contrib.auth import
from django.db.models.signals import post_save,pre_save
from Guest.models import Guest
import stripe
# from Address.models import Address

from django.urls import reverse

USER=settings.AUTH_USER_MODEL

stripe.api_key=getattr(settings,'STRIPE_API_Key')
# stripe.api_key="sk_test_D4RgyaK4XRnGuFPKOoJ4eKst"

class BillingManager(models.Manager):

    def get_or_new(self,request):
        guest_id = request.session.get('guest_id')
        user=request.user
        billing_profile = None
        if request.user.is_authenticated:
            billing_profile, billing_profile_created = self.get_queryset().get_or_create(user=user, email=user.email)

        elif guest_id is not None:

            Guest_obj = Guest.objects.get(id=guest_id)
            billing_profile, billing_guest_profile_created = self.get_queryset().get_or_create(email=Guest_obj.email)

        return billing_profile

class billing(models.Model):

    user   = models.OneToOneField(USER,null=True,blank=True,on_delete=models.CASCADE)
    timestamp= models.DateTimeField(auto_now_add=True)
    update=models.DateTimeField(auto_now=True)
    email=models.EmailField()
    active = models.BooleanField(default=True)
    customer_id=models.CharField(max_length=255,blank=True,null=True)

    objects=BillingManager()

    def __str__(self):
        return self.email


    def process_charge(self,order_obj):
        # print(self)
        return Charge.objects.do_charge(self,order_obj)

    def get_cards(self):
        return self.card_set.all()    # ia have modified in default all() function and now is equivalnt to self.objects.all().filter(active==True)

    def get_payment_method_url(self):
        return reverse('billing:payment-method-change')


    @property
    def has_card(self):
        qs=self.get_cards()
        if qs.exists():
            return True
        return False

    @property
    def default_cards(self):
        qs=self.get_cards().filter(default=True)
        if qs.exists():
            return qs.first()
        return None

    # @property    # mainly used this function for guest user ,  replaced it with postsave signal in address
    # def set_card_inactive(self):
    #     qs=self.get_cards()
    #     if qs.exists():
    #         qs.update(active=False)


def customer_id_creation(sender,instance,*args,**kwargs):
    print("integrating with strip API, new customer is created in stripe before saving billing profile for "+str(instance.email))
    instance.customer_id=stripe.Customer.create(
        email=instance.email,
        description="Customer for {email}".format(email=instance.email)

    ).id
    print(instance.customer_id)

pre_save.connect(customer_id_creation,sender=billing)

def user_created_billing_created(sender,instance,created,*args,**kwargs):
    # print("the settings.AUTH_USER_MODEL object="+USER)
    if created and instance.email:
        billing_obj=billing.objects.create(user=instance,email=instance.email) # change it from get_or_create to create
        # print(billing_obj)


post_save.connect(user_created_billing_created,sender=USER)


class CardManager(models.Manager):

    def all(self,*args,**kwargs):
        return self.get_queryset().filter(active=True)   # i made it self.get_queryset().all().filter(active=True) but it was incorrect as i modify on the default all function

    def new_card(self,billing,token):

        if token:
            customer = stripe.Customer.retrieve(billing.customer_id)
            card_response = customer.sources.create(source=token)
            return self.get_queryset().create(billing=billing,stripe_id=card_response.id,
                                   brand=card_response.brand,country=card_response.country,exp_month=card_response.exp_month,
                                   exp_year=card_response.exp_year,last4=card_response.exp_year)
        return None

class Card(models.Model):
    billing      = models.ForeignKey(billing,on_delete=models.CASCADE)
    stripe_id    = models.CharField(max_length=225)
    brand        = models.CharField(max_length=120,null=True,blank=True)
    country      = models.CharField(max_length=120,null=True,blank=True)
    exp_month    = models.IntegerField(null=True, blank=True)
    exp_year     = models.IntegerField(null=True, blank=True)
    last4        = models.IntegerField(null=True, blank=True)
    default      = models.BooleanField(default=True)
    active       =models.BooleanField(default=True)
    timestamp    =models.DateTimeField(auto_now_add=True)



    objects=CardManager()

    def __str__(self):
        return "{brand}{last4}".format(brand=self.brand,last4=self.last4)



def let_default_False_cards(sender,instance,created,*args,**kwargs):
    if created:
        card_qs=Card.objects.filter(billing=instance.billing,default=True).exclude(pk=instance.pk)
        if card_qs.exists():
            card_qs.update(default=False)   #will update all the items in the queryset

post_save.connect(let_default_False_cards,sender=Card)





class ChargeManager(models.Manager):

    def do_charge(self,billing_profile,order_obj,card_obj=None):

        if card_obj is None:
            card_qs=billing_profile.card_set.filter(default=True)
            if card_qs.exists():
                card_obj=card_qs.first()
        if card_obj is None:
            return False
        charge_obj = stripe.Charge.create(
            amount=int(order_obj.total)*100,
            currency="usd",
            customer=billing_profile.customer_id,
            source=card_obj.stripe_id,  # obtained with Stripe.js
            metadata={"order_id":order_obj.order_id},
            description="Charge for " + str(billing_profile)
        )
        print(charge_obj)
        return self.get_queryset().create(billing=billing_profile,stripe_id=charge_obj.id,
                                   paid=charge_obj.paid,refunded=charge_obj.refunded,outcome=charge_obj.outcome,
                                   outcome_type=charge_obj.outcome['type'],seller_message=charge_obj.outcome.get('seller_message'),
                                   risk_level=charge_obj.outcome.get('risk_level'))

class Charge(models.Model):
    billing       = models.ForeignKey(billing, on_delete=models.CASCADE)
    stripe_id     = models.CharField(max_length=225)
    paid          = models.BooleanField(default=False)
    refunded      = models.BooleanField(default=False)
    outcome       = models.TextField(null=True,blank=True)
    outcome_type  = models.CharField(max_length=120,null=True,blank=True)
    seller_message= models.CharField(max_length=120,null=True,blank=True)
    risk_level    = models.CharField(max_length=120,null=True,blank=True)



    objects=ChargeManager()