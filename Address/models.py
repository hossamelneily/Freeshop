from django.db import models
from billing.models import billing
from billing.models import Card
from django.db.models.signals import post_save,pre_save


ADRESS_TYPES=(
    ("billing","Billing"),
    ("shipping","Shipping")
)


class Address(models.Model):

    billing        = models.ForeignKey(billing,on_delete=models.CASCADE)
    Address_Type   = models.CharField(max_length=250,choices=ADRESS_TYPES)
    Address_line_1 = models.CharField(verbose_name='Address1',max_length=250)
    Address_line_2 = models.CharField(verbose_name='Address2',max_length=250,null=True,blank=True)
    State          = models.CharField(verbose_name='State',max_length=250,default="kuwait")
    Postal_Code    = models.CharField(verbose_name='Postal Code',max_length=250)
    city           = models.CharField(verbose_name='City',max_length=250)
    ContactNo      =models.CharField(verbose_name='Contact Number',max_length=250)
    FullName       =models.CharField(verbose_name='Full Name',max_length=250,default='hossam')


    def __str__(self):
        # print(type(self.billing))
        return str(self.billing)


    def get_address(self):
        return "{line1}\n{line2}\n{state},{postal}\n{city}".format(
            line1=self.Address_line_1,
            line2=self.Address_line_2 or "",
            state=self.State,
            postal=self.Postal_Code,
            city=self.city

        )



def let_inactive_guestUser_cards(sender,instance,created,*args,**kwargs):
    if created and not instance.billing.user:
        card_qs = Card.objects.filter(active=True,billing__user=None)
        if card_qs.exists():
            card_qs.update(active=False)   #will update all the items in the queryset
post_save.connect(let_inactive_guestUser_cards,sender=Address)