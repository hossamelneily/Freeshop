
from django.conf.urls import include,url

from cart.views import checkout_view
from .views import paymentMethod,paymentMethodCreate

app_name="billing"

urlpatterns = [

    url('^payment-method/$', paymentMethod, name="payment-method"),
    url('^payment-method/create/$', paymentMethodCreate, name="payment-method-create"),
    url('^payment-method/change/$', checkout_view, name="payment-method-change"),
]

