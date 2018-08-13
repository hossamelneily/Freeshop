
from django.conf.urls import include,url
from . import views

from .views import ( SearchProductView)

app_name="search"

urlpatterns = [

   url('^$',SearchProductView.as_view(),name="query"),


]

