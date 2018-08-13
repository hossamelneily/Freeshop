
from django.conf.urls import include,url
from . import views

from .views import cart_view,cart_update,checkout_view,checkout_done,cart_view_API
from Address.views import Adress_Use_Prev,AddressView,UsePrevAddress
app_name="cart"

urlpatterns = [

   url('^$',cart_view,name="show"),
   url('^update/$',cart_update,name="update"),
   url('^checkout/$',checkout_view,name="checkout"),
   url('^checkout/Address/$',AddressView.as_view(),name="checkout-Address"),
   url('^checkout/Address/reuse$',UsePrevAddress.as_view(),name="checkout-Address-reuse"),
   url('^checkout/success$',checkout_done,name="success"),


   #AJax urls:
  # url('^api/show/$',cart_view_API,name="cart_show_API")

]

