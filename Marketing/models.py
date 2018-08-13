from django.db import models

from django.db.models.signals import post_save,pre_save
from .utils import Mailchimp
from django.conf import settings



class MarketingPreference(models.Model):
    user       = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    subscribed = models.BooleanField(default=True)
    mailchimp_msg = models.TextField(null=True,blank=True)
    timestamp= models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)




    def __str__(self):
        return self.user.email



def marketing_pref_subscription(sender,instance,*args,**kwargs):
    if instance.subscribed:
        status_code, data = Mailchimp().subscribed(instance.user.email)
    else:
        status_code, data = Mailchimp().unsubscribed(instance.user.email)
    instance.mailchimp_msg=data
    print(status_code,data)
pre_save.connect(marketing_pref_subscription,sender=MarketingPreference)




def marketing_pref_creating(sender,instance,created,*args,**kwargs):
    if created:
        status_code,data=Mailchimp().add_email(email=instance.user.email)
        print(status_code,data)

post_save.connect(marketing_pref_creating,sender=MarketingPreference)



def marketing_pref_creation_receiver(sender,instance,created,*args,**kwargs):
    if created:
        MarketingPreference.objects.get_or_create(user=instance)

post_save.connect(marketing_pref_creation_receiver,sender=settings.AUTH_USER_MODEL)




