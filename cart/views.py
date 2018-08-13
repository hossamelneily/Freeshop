from django.shortcuts import render,redirect
from django.contrib.auth import authenticate , login , get_user_model
from django.conf import settings
# Create your views here.
from cart.models import cart
from products.models import product
from products.models import product
from orders.models import orders
from ecommerce.forms import login_page,GuestForm
from billing.models import billing
from Address.models import Address
from Guest.models import Guest
from django.urls import reverse
from Address.forms import AdressForm,UsePrevAdd
from django.http import JsonResponse
import json
user=get_user_model()



def cart_view_API(request):
    cart_obj = cart.objects.get_or_create(request)
    product = cart_obj.products.all()
    product_list=[]
    for x in product:
        product_list.append({"name":x.Name,"price":x.price,"url":x.get_absolute_url(),"id":x.id})
    return JsonResponse({ "product": product_list,
                          "cart_total": cart_obj.total,
                          "cart_subtotal":cart_obj.subtotal
                         })

def cart_view(request):

    # i have created a function in the carts.models and i will call it instead of implementing it here.
    cart_obj=cart.objects.get_or_create(request)
    return render(request,"carts/home.html",{"cart_obj":cart_obj})


def cart_update(request):


     prod_obj=product.objects.get_by_id(id=request.POST.get('product_id'))
     cart_obj = cart.objects.get_or_create(request)

     if  prod_obj in cart_obj.products.all():
         cart_obj.products.remove(prod_obj)
         added=False
     else:
         cart_obj.products.add(prod_obj)
         added=True
     request.session['cart_items']=cart_obj.products.count()
     if request.is_ajax():                                       # will return json format
         print("Ajax is working ")
         json_data={
             "added":added,
             "cart_items_count":request.session.get("cart_items",0)

         }
         return JsonResponse(json_data)
     return redirect("cart:show")    # need to modify this return


def checkout_view(request):


    cart_obj = cart.objects.get_or_create(request)

    order_obj=None
    Address_qs=None
    prev_form_shipping = None
    prev_form_billing = None
    Shipping_Address_qs = None
    Billing_Address_qs = None
    loginform = login_page(request.POST or None)
    guestform = GuestForm(request.POST or None)
    adressForm = AdressForm(request.POST or None)
    has_card = None
    # change =None

    billing_profile= billing.objects.get_or_new(request)



    if billing_profile is not None:
        order_obj, order_created = orders.objects.get_or_new(billing_profile, cart_obj)
        order_obj.Associate_orders_to_Addresses(request)

        if request.user.is_authenticated:
            Address_qs=Address.objects.filter(billing=billing_profile)
            Shipping_Address_qs = Address_qs.filter(Address_Type='shipping').values('id','Address_line_1','State','Postal_Code','city').distinct()
            #values('id','Address_line_1','State','Postal_Code','city')  --> i have added the id beacuse we need to save the id of the address
            #but if the addresses all have the same values, this query will return the same addresses even we make ditinct beacuse their ids are different
            #so the user have to add different address to return different ones,
            if Shipping_Address_qs:
                prev_form_shipping = UsePrevAdd(request.POST or None,initial={'Address_Type':'shipping'})
            Billing_Address_qs = Address_qs.filter(Address_Type='billing').values('id','Address_line_1','State','Postal_Code','city').distinct()
            if Billing_Address_qs:
                prev_form_billing = UsePrevAdd(request.POST or None,initial={'Address_Type':'billing'})


        # if 'change' in request.build_absolute_uri():
        #     print('changes')
        #     change =True
        #     return redirect("cart:checkout")
        has_card=billing_profile.has_card  # get the active cards

    if request.method=="POST" and not request.is_ajax():    #came from checkout() function when user entered all addresses and payement method, last step
        is_done = order_obj.check_orders()
        if is_done:
            did_charge = billing_profile.process_charge(order_obj=order_obj)
            if did_charge:
                order_obj.mark_paid()
                del request.session['cart_id']
                request.session['cart_items'] = 0
                # if not billing_profile.user:       #not means false or None   # is None means None only this for guest user
                #     billing_profile.set_card_inactive
                return redirect("cart:success")
            return redirect("cart:checkout")






    context={
        "cart_obj":cart_obj,
        "object": order_obj,
        "billing_profile":billing_profile,
        "loginpage":loginform,
        "guestform":guestform,
        "addressform":adressForm,
        'prev_form_shipping':prev_form_shipping,
        'prev_form_billing': prev_form_billing,
        "Address_qs":Address_qs,
        'Shipping_Address_qs':Shipping_Address_qs,
        'Billing_Address_qs':Billing_Address_qs,
        "has_card":has_card,
        # 'change':change,
        "public_key":getattr(settings,'STRIPE_PUB_Key','pk_test_UmKYvEdkBYpow9jUa9gloSTC')


    }

    return render(request,"carts/checkout.html",context)


def checkout_done(request):
    return render(request, "carts/success.html", {})
