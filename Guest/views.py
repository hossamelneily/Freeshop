from django.shortcuts import render
from django.views.generic import CreateView,FormView,UpdateView,View
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse,HttpResponse
from .models import EmailActivaion
from django.conf import settings
from Marketing.mixins import CsrfExemptMixin
from django.contrib import messages
from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse
from django.utils.html import mark_safe
from django.views.generic.edit import FormMixin
from .forms import EmailReactivation
# Create your views here.


class EmailActivationView(FormMixin,CsrfExemptMixin,View):
    form_class = EmailReactivation
    success_url = '/login'
    key=None

    def get(self,request,key=None,*args,**kwargs):   # self will print Em
        # print(self.__class__)
        self.key=key
        # print(self.key)
        # print("teeeeeeeeeeeeeeeeeeee="+str(self))
        if key is not None:
            qs=EmailActivaion.objects.filter(key__iexact=key)
            qs_confirmable = qs.confirmable()
            #to activate your email account
            if qs_confirmable.exists():
                if qs_confirmable.first().activate():
                    messages.success(request,"your account has been activated please login")
                    return redirect('login')
            # if already activated reset password page
            else:
               activated_qs=qs.filter(activated=True)
               if activated_qs.exists():
                    reset_link=reverse('password_reset')
                    msg='''
                        your email has already been confirmed , Do you want to <a href='{link}'>reset your password?</a> 
                        '''.format(link=reset_link)
                    messages.success(request,mark_safe(msg))
                    return redirect('login')
        #if error
        context={
            'form':self.get_form(),
            'key':key
        }
        return render(request,'registration/activation_error.html',context)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # Here, we would record the user's interest using the message
        # passed in form.cleaned_data['message']
        #resend only activation mail
        msg='''
            Activation mail sent , please check your email
        '''
        messages.success(self.request,msg)
        obj = EmailActivaion.objects.filter(email__iexact=form.cleaned_data.get('email')).first()
        obj.Send_Activation_Email()
        # obj.activate()
        return super().form_valid(form)

    def form_invalid(self, form):
        # if error
        context = {
            'form': self.get_form(),
            'key':self.key
        }
        return render(self.request, 'registration/activation_error.html', context)
