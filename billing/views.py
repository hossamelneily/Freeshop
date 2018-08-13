from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.utils.http import is_safe_url
from billing.models import billing,Card,Charge
from django.conf import settings
from orders.models import orders
import stripe

STRIPE_PUB_Key = getattr(settings,'STRIPE_PUB_Key')

def paymentMethod(request):

    if request.user.is_authenticated:
        # print(request.user.billing.customer_id)
        billing_profile= billing.objects.get_or_new(request=request)
        # print(billing_profile.customer_id)
        # print(request.POST.get("token",None))

    next_ = request.GET.get("next")
    next_post = request.POST.get("next")
    redirected_path = next_ or next_post
    next_url =None
    if is_safe_url(redirected_path, request.get_host()):
        next_url=next_ or next_post
    context={
        'public_key':STRIPE_PUB_Key,
        'next_url':next_url,
        'show_navbar':'base.html'
    }

    return render(request,'payment2.html',context)


def paymentMethodCreate(request):
    if request.method == 'POST' and request.is_ajax():    # came from ajax, when user click the btn for payment
        billing_profile = billing.objects.get_or_new(request=request)
        if billing_profile and request.POST.get("token") is not None:
            Card.objects.new_card(billing=billing_profile,token=request.POST.get("token"))
            # i have made this function in the Charge model and make modemanager then called do_charge in the checkout view
        return JsonResponse({"message":"succes and your request is processing "})
    return HttpResponse("error",status=400,content_type="application/json")





