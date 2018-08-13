from django.db import models
from django.conf import settings
from products.models import product
from django.db.models.signals import m2m_changed
import math

User = settings.AUTH_USER_MODEL



class CartManager(models.Manager):



    def cart_create(self,user=None):
        user_obj = None

        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.get_queryset().create(user=user_obj)

    def get_or_create(self,request):

        username = request.user
        cart_id = request.session.get('cart_id', None)

        print("username="+str(username))
        if cart_id is None:
            print("New user")
            cart_obj = cart.objects.cart_create(user=request.user)
            request.session['cart_id'] = cart_obj.id
        else:
            print("cart already exists")
            print(cart_id)
            cart_obj = cart.objects.get(id=cart_id)
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        return cart_obj

class cart(models.Model):

    user      = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.CASCADE)
    products  = models.ManyToManyField(product, blank=True)
    subtotal  = models.DecimalField(decimal_places=2, max_digits=20, default=0.00)
    total     = models.DecimalField(decimal_places=2, max_digits=20, default=0.00)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated   = models.DateTimeField(auto_now=True)


    objects=CartManager()

    def __str__(self):
        return str(self.id)

def cal_total(sender,instance,action,*args,**kwargs):
    # print(action)
    if action=="post_add" or action=="post_remove" or action=="post_clear":
        prod_objs=instance.products.all()
        subtotal=0
        for prod in prod_objs:
            subtotal+=prod.price
        # print(subtotal)
        total=math.fsum([subtotal,10])
        instance.total=total
        instance.subtotal=subtotal
        instance.save()


m2m_changed.connect(cal_total, sender=cart.products.through)




