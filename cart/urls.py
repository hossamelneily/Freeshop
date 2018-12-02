
from django.conf.urls import include,url
from . import views

from .views import cart_view,cart_update,checkout_view,checkout_done,cart_view_API,Get_Cart_API,Remove_from_cart_Modal
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
   url('^api/get_cart/$',Get_Cart_API,name="Get_Cart_API"),
   url('^api/remove_form_cart/$',Remove_from_cart_Modal,name="Remove_form_cart"),


  # url('^api/show/$',cart_view_API,name="cart_show_API")

]


