from django.shortcuts import render
from django.views.generic import CreateView,FormView,UpdateView,View
from .forms import MarketingPreferencesForm
from .models import MarketingPreference
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse,HttpResponse
from .utils import Mailchimp
from django.conf import settings
from.mixins import CsrfExemptMixin
# from requestbin.bin import Bin
MAILCHIMP_EMAIL_LIST_ID = getattr(settings,"MAILCHIMP_EMAIL_LIST_ID",None)


#SuccessMessageMixin   --> is used for meassaging the user for the result i copied and paste it from the video as it is
class MarketingPreferencesView(SuccessMessageMixin,UpdateView):
    form_class = MarketingPreferencesForm
    template_name = 'base/forms.html'
    success_url = '/settings/email'
    success_message = "your email preferences have been updated successfully"

    def get_object(self, queryset=None):
        obj= MarketingPreference.objects.get(user=self.request.user)
        # myBin=Bin.create()
        # print(myBin)
        print(obj)
        return obj


    def get_context_data(self, *args,**kwargs):
        context=super().get_context_data(*args,**kwargs)
        context['title']="Update Email Preferences"
        print(context.get('form',None))
        return context



# didn't test it yet as we don't have live url yet ,  we used CsrfExemptMixin for csrf
class MailChimpWehbookView(CsrfExemptMixin,View):
    def post(self,request,*args,**kwargs):
        type = request.POST.get('type', None)
        list_id = request.POST.get('data%5Blist_id%5D', None)
        if str(list_id) == str(MAILCHIMP_EMAIL_LIST_ID):
            email = request.POST.get('data%5Bemail%5D', None)
            response_status, response_data = Mailchimp().check_email(email)
            if response_data['status'] == 'subscribed':
                qs = MarketingPreference.objects.filter(user__email__iexact=email)
                if qs.exists():
                    qs.update(subscribed=True, mailchimp_msg=request.POST)
            if response_data['status'] == 'unsubscribed':
                qs = MarketingPreference.objects.filter(user__email__iexcact=email)
                if qs.exists():
                    qs.update(subscribed=False, mailchimp_msg=request.POST)
        return HttpResponse("Thank you", status=200)

# def MailChimpWehbookView(request): we have changed the fbv to cbv above

'''
type=unsubscribe&
fired_at=2018-04-18+22%3A15%3A36&
data%5Breason%5D=manual&
data%5Bid%5D=4c757c941a&
data%5Bemail%5D=h1%40gmail.com&
data%5Bemail_type%5D=html&
data%5Bip_opt%5D=37.34.172.141&
data%5Bweb_id%5D=3430347&
data%5Bmerges%5D%5BEMAIL%5D=h1%40gmail.com&
data%5Bmerges%5D%5BFNAME%5D=&
data%5Bmerges%5D%5BLNAME%5D=&
data%5Bmerges%5D%5BADDRESS%5D=&
data%5Bmerges%5D%5BPHONE%5D=&
data%5Bmerges%5D%5BBIRTHDAY%5D=&
data%5Blist_id%5D=1130804d65
'''
