from django.db import models


from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from .signals import object_viewed_signal
from Guest.signals import User_logged_in
from .utils import get_IP
from django.contrib.sessions.models import Session
from django.db.models.signals import post_save,pre_save
User = settings.AUTH_USER_MODEL



FORCE_SESSION_TO_ONE=getattr(settings,'FORCE_SESSION_TO_ONE',False)
FORCE_USER_TO_DEACTIVATE=getattr(settings,'FORCE_USER_TO_DEACTIVATE',False)


class ObjectView(models.Model):
    user=models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)
    IPAddress = models.CharField(max_length=225)
    content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id=models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id')
    timestamp=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return "{contentObject} viewed on {timestamp}".format(contentObject=self.content_object,timestamp=self.timestamp)


    class Meta:
        ordering=['-timestamp']
        verbose_name= 'Object viewed'
        verbose_name_plural= 'Objects viewed'



class UserSession(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    IPAddress = models.CharField(max_length=225)
    sessionkey=models.CharField(max_length=100,blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    active=models.BooleanField(default=True)
    ended=models.BooleanField(default=False)




    def end_session(self):
        try:
            session=Session.objects.get(pk=self.sessionkey).delete()
            #print("end session"+ session)
            self.active=False
            self.ended=True
            self.save()
        except:
            pass
        return self.ended


def post_save_end_session(sender,instance,created,*args,**kwargs):
    if created:
        print("session just created")
        #print(instance.sessionkey)
        qs=UserSession.objects.filter(user=instance.user,active=False,ended=False).exclude(id=instance.id) #means the user is deactivated but still the session is open
    for i in qs:
        i.end_session()

if FORCE_SESSION_TO_ONE:
    post_save.connect(post_save_end_session,sender=UserSession)


def post_save_user_deactivate(sender,instance,created,*args,**kwargs):
    if not created:
        if not instance.is_active:
            qs = UserSession.objects.filter(user=instance, active=False, ended=False)
            for i in qs:
                i.end_session()

if FORCE_USER_TO_DEACTIVATE:
    post_save.connect(post_save_user_deactivate,sender=User)


def Object_View_receiver(sender,instance,*args,**kwargs):
    print("my custom signal is working fine")
    # print(instance)                                           #product
    # print(kwargs.get('request'))
    # print(sender)                                             #<class 'products.models.product'>
    # print(ContentType.objects.get_for_model(sender))
    # print("test instance   = "+str(instance.__class__))
    user=None
    if kwargs.get('request').user.is_authenticated:
        user=kwargs.get('request').user
    object_viewed_obj=ObjectView.objects.create(
        user=user,
        IPAddress=get_IP(kwargs.get('request')),
        content_type=ContentType.objects.get_for_model(sender),   #as intance.__class__
        object_id=instance.id
    )
    # object_viewed_signal.save()


object_viewed_signal.connect(Object_View_receiver)



def User_logged_in_receiver(sender,instance,*args,**kwargs):
    print("custom user logged signal is wokring")
    # print(sender)
    # print(instance)
    #print(dir(kwargs.get(('request')).session))
    # print(kwargs.get(('request')).session.session_key)
    request_session=kwargs.get(('request')).session
    if not kwargs.get(('request')).session.session_key:
        kwargs.get(('request')).session.save()
    UserSession.objects.create(
        user=instance,
        IPAddress=get_IP(kwargs.get('request')),
        sessionkey=kwargs.get(('request')).session.session_key
    )
    print("still in custom user logged in signal")
    # print(dir(kwargs.get(('request')).session))
    # print((request_session.keys()))

    # print("working"+str(Session.objects.get(pk=kwargs.get(('request')).session.session_key)))

User_logged_in.connect(User_logged_in_receiver)