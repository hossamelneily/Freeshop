
from django.conf.urls import include,url
from . import views

from ecommerce.views import AccountHomeView
from Guest.views import EmailActivationView

app_name="Guest"

urlpatterns = [



   url('^$', AccountHomeView.as_view(),name="home"),
   url(r'^email/activate/(?P<key>[0-9A-Za-z]+)/$', EmailActivationView.as_view(),name="email_activated"),
   url(r'^email/reactivate/$', EmailActivationView.as_view(),name="email_reactivate"),
]

