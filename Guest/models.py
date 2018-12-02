from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.db.models.signals import post_save,pre_save
from products.utils import unique_key_generator
from django.core.mail import send_mail
from django.template.loader import get_template
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse
from django.contrib.auth import get_user_model

from django.contrib import messages

User = get_user_model()


DEFAULT_EXPIRATION_DAYS=getattr(settings,'DEFAULT_EXPIRATION_DAYS',7)

class EmailActivaionQuerySet(models.query.QuerySet):
    def confirmable(self):
        start_date = timezone.now() - timedelta(days=DEFAULT_EXPIRATION_DAYS)  # now - 7 days --> start will return back to the past
        end_date  = timezone.now()                                             #will be now -->
        #check is timestamp between start_date & end_date
        return self.filter(activated=False,forced_expired=False).filter(
            timestamp__gt=start_date , timestamp__lte=end_date )      # this will make and condition

    def check_active(self):
        return self.filter(activated=True,user__is_active=True)


class EmailActivaionManager(models.Manager):

    def confirmable(self):
        return self.get_queryset().all().confirmable()

    def get_queryset(self):
        return EmailActivaionQuerySet(self.model,using=self._db)

class EmailActivaion(models.Model):
    user =          models.OneToOneField(User,on_delete=models.CASCADE)
    email =         models.EmailField()
    key =           models.CharField(max_length=255)
    timestamp =     models.DateTimeField(auto_now_add=True)
    updated =       models.DateTimeField(auto_now=True)
    activated =     models.BooleanField(default=False)
    forced_expired= models.BooleanField(default=False)
    expires=        models.IntegerField(default=DEFAULT_EXPIRATION_DAYS)  #7 days

    def __str__(self):
        return self.user.email

    objects=EmailActivaionManager()

    def activate(self):
        qs=EmailActivaion.objects.filter(id=self.id).confirmable()
        if qs.exists():
            self.user.is_active=True
            self.user.save()
            self.activated =True
            self.save()
            return True
        return False



    def Send_Activation_Email(self):
        subject = "FreeShop Account Activation"
        rev_link=reverse('Accounts:email_activated',kwargs={'key':self.key})
        path = '{Base_urL}{rev}'.format(Base_urL=settings.BASE_URL,rev=rev_link)
        # print(path)
        context = {'email': self.email, 'path': path}
        txt_ = get_template('registration/emails/verify.txt').render(context)
        html_ = get_template('registration/emails/verify.html').render(context)
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [self.email, from_email]
        # messages.success(self.request, "Activation mail has been sent, kindly check your Email")
        send_mail(subject, txt_, from_email, recipient_list,html_message= html_, fail_silently=False)

def Key_Activation_reciever(sender,instance,*args,**kwargs):
    if not instance.key:
        instance.key=unique_key_generator(instance)

pre_save.connect(Key_Activation_reciever,sender=EmailActivaion)


def Send_Activation_Email_reciever(sender,instance,created,*args,**kwargs):
    if created :
        # pass
        obj = EmailActivaion.objects.create(user=instance, email=instance.email)
        obj.Send_Activation_Email()
        # print("from model of email activation"+obj.key)

post_save.connect(Send_Activation_Email_reciever,sender=User)



class Guest(models.Model):

    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)


    def __str__(self):
        return self.email
