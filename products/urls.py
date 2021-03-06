

from django.conf.urls import include,url
from . import views

from .views import (
   ProductlistView,
   ProductDetailSlugView,
   MainProductlistView

)

app_name="products"
urlpatterns = [

   url('^$',ProductlistView.as_view(),name="list"),
   url(r'^list/(?P<category>[\w-]+)/$',MainProductlistView.as_view(),name='category'),


   # the detail view for teh products
   url(r'^(?P<slug>[\w-]+)/$',ProductDetailSlugView.as_view(),name='detail')



]


