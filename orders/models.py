from django.db import models
from django.db.models.signals import pre_save,post_save
from cart.models import cart
from products import utils
from billing.models import billing
from Address.models import Address
import math
Order_Status_Choices=(
    ('created','Created'),
    ('shipped','Shipped'),
    ('paid','Paid'),
    ('canceled','Canceled')
)

class OrderManager(models.Manager):

    def get_or_new(self,billing_profile,cart_obj):
        order_obj = None
        #  the old version of order creation
        order_qs = self.get_queryset().filter(billing_profile=billing_profile, cart=cart_obj, active=True)
        if order_qs.count() == 1:
            print("test1")
            order_obj = order_qs.first()
            order_created=False
        else:
            order_created=True
            print("test2")
            order_obj = self.get_queryset().create(billing_profile=billing_profile, cart=cart_obj)

        return  order_obj,order_created

class orders(models.Model):

    order_id         = models.CharField(blank=True,max_length=25,unique=True)
    cart             = models.ForeignKey(cart,on_delete=models.CASCADE)
    status           = models.CharField(max_length=25,default='created',choices=Order_Status_Choices)
    shipping_total   = models.DecimalField(decimal_places=2, max_digits=20, default=5.00)
    total            = models.DecimalField(decimal_places=2, max_digits=20, default=0.00)
    billing_profile  = models.ForeignKey(billing,null=True,on_delete=models.CASCADE)
    active           = models.BooleanField(default=True)
    shipping_Address = models.ForeignKey(Address,related_name="shipping_Address",on_delete=models.CASCADE,null=True)
    Billing_Address  = models.ForeignKey(Address,related_name="Billing_Address",on_delete=models.CASCADE,null=True)

    objects=OrderManager()


    def Associate_orders_to_Addresses(self,request):


        shipping_Address_id = request.session.get("shipping_address_id", None)

        if shipping_Address_id:
            self.shipping_Address=Address.objects.get(id=shipping_Address_id)
            del request.session["shipping_address_id"]


        billing_Address_id = request.session.get("billing_address_id", None)

        if billing_Address_id:
            self.Billing_Address=Address.objects.get(id=billing_Address_id)
            del request.session["billing_address_id"]

        if shipping_Address_id or billing_Address_id:
            self.save()

    def mark_paid(self):
        if self.check_orders():
            self.status = "paid"
            self.save()
        return self.status

    def check_orders(self):
        billing_profile=self.billing_profile
        shipping_Address = self.shipping_Address
        Billing_Address=self.Billing_Address
        total = self.total

        if billing_profile and shipping_Address and Billing_Address and total>0:
            return True
        return False

    def __str__(self):
        return self.order_id

    def update_total(self):
        # print("wefweffffffffffffffffffffd"+self.cart.total)
        # print(type(self.shipping_total))
        new_total=math.fsum([self.cart.total,self.shipping_total])  # as one is float and the other is decimal
        fomratted_total=format(new_total,'.2f')
        self.total=fomratted_total
        self.save()
        # return self.total


#generete order id

def presave_order_id(sender,instance,*args,**kwargs):
    if not instance.order_id:
        instance.order_id=utils.unique_order_id_generator(instance)

    qs = orders.objects.filter(cart=instance.cart,active=instance.active).exclude(billing_profile=instance.billing_profile)  # in case the guest user become login user, even after he continue as a guest
    if qs.exists():
        print("test3")
        qs.update(active=False)


pre_save.connect(presave_order_id,sender=orders)


def postsave_cart_total(sender,instance,created,*args,**kwargs):  # in every time the cart changes
    if  not created:
        print("postsave cart total")
        cart_obj=instance
        order_qs=orders.objects.filter(cart__id=cart_obj.id)
        if order_qs.exists():
            print(order_qs)
            order_obj=order_qs.first()
            order_obj.update_total()

post_save.connect(postsave_cart_total,sender=cart)


# generate order total
def postsave_order_total(sender,instance,created,*args,**kwargs):  # in this case when the order first created
    if  created:
        print("just order created ")
        instance.update_total()

post_save.connect(postsave_order_total,sender=orders)