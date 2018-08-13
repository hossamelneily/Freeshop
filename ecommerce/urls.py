"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.conf.urls import include,url
from . import views

from .views import RegisterView,LoginView,account_home_view,GuestView
from django.views.generic import TemplateView,RedirectView
from django.contrib.auth.views import LogoutView
from cart.views import  cart_view_API
from billing.views import paymentMethod,paymentMethodCreate
from Marketing.views import MarketingPreferencesView,MailChimpWehbookView
# from django.urls import path
# from products.views import (
#    ProductlistView,
#    Productfnc ,detailfnc,
#    productdetailview,
#    ProductDetailSlugView,
#    FeaturedProductlistView,
#    FeaturedProductDetailView)


urlpatterns = [

   url('^products/', include("products.urls",namespace="product")),




   url('^search/', include("search.urls",namespace="search")),
   url('^cart/', include("cart.urls",namespace="cart")),
   url('admin/', admin.site.urls),


   url('^$', views.home_page,name="home"),   #this usrl will be changed to below url
   #need to redirectview
   # url('^accounts/', RedirectView.as_view(url='/account')),
   url('^account/', include("Guest.urls",namespace="Accounts")),
   url('^accounts/', include("Guest.password.urls")),


#Stripe URls
   url('^billing/',include("billing.urls",namespace="billing")),
   # url('^billing/payment-method/$',paymentMethod,name="payment-method"),
   # url('^billing/payment-method/create$', paymentMethodCreate, name="payment-method-create"),


   url('^contact/$', views.contact_page,name="contact"),
   url('^about/$', views.about_page,name="about"),
   url('^FAQ/$', views.FAQ,name="FAQ"),
   # url('^login/$', views.loginfn,name="login"),           # converted it to class based view
   url('^login/$', LoginView.as_view(),name="login"),


   url('^register/guest$', GuestView.as_view(),name="guest_url"),
   # url('^register/guest$', views.guestfnc,name="guest_url"),


   # url('^logout/$', views.logout,name="logout"),
   url('^logout/$', LogoutView.as_view(),name="logout"),
   # url('^register/$', views.register,name="register"),       # converted it to class based view

   url('^register/$', RegisterView.as_view(),name="register"),



   url('^bootstrap/$', TemplateView.as_view(template_name="bootstrap/bootstrap.html")),    # templateview to test the bootstrap , it doesn't have views
   # url('^product/$',ProductlistView.as_view()),
   # url('^productfnc/$',Productfnc),
   # url(r'^productfnc/(?P<album_id>\d+)/$',detailfnc),
   # url(r'^product/(?P<pk>\d+)/$',productdetailview.as_view()),
   #
   # url('^featured-prd/$',FeaturedProductlistView.as_view()),
   # url('^featured-prd/(?P<pk>\d+)/$',FeaturedProductDetailView.as_view()),
   #
   # url(r'^product/(?P<slug>[\w-]+)/$',ProductDetailSlugView.as_view()),

   #AJAX Urls:
   url('^api/show/$',cart_view_API,name="cart_show_API"),








   #Mailchimp integraion
   url('^settings/email/$',MarketingPreferencesView.as_view(),name="Marketing-preference"),
   url('^webhook/mailchimp/$',MailChimpWehbookView.as_view(),name="webhook-mailchimp"),

]

if settings.DEBUG:
   urlpatterns = urlpatterns+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
   urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
