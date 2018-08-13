from django.shortcuts import render,redirect
from .forms import AdressForm,UsePrevAdd
from django.utils.http import is_safe_url
from billing.models import billing
from django.views.generic import CreateView,FormView
from django.views.generic.edit import ProcessFormView
from ecommerce.mixins import NextUrlMixin



class AddressView(NextUrlMixin,CreateView):
    form_class = AdressForm
    template_name = 'Shipping&Billing Adresses/snippets/form.html'
    def get_success_url(self):
        return self.get_next_url()

    def get_form_kwargs(self,*args,**kwargs):
        kwargs=super().get_form_kwargs(*args,**kwargs)
        kwargs['request']= self.request
        return kwargs

    # def form_valid(self, form):
    #     form.save()
    #     return redirect(self.get_success_url())


    def form_invalid(self, form):
        print(form.errors)
        print('Errors in Form Invalid function of AddressView')
        return redirect('/')


class UsePrevAddress(NextUrlMixin,FormView):

    form_class = UsePrevAdd
    template_name = 'Shipping&Billing Adresses/snippets/prev_Add.html'


    def form_valid(self, form):
        print("test5")
        self.request.session[self.request.POST.get('Address_Type', "") + "_address_id"] = self.request.POST.get("Address-id")
        return redirect(self.get_next_url())

    def form_invalid(self, form):
        print(form.errors)
        print('Errors in Form Invalid function of UsePrevAddress')
        super().form_invalid(form)
        # return redirect('/')

def Adress_Use_Prev(request):



    # print(request.POST)
    address_type=request.POST.get('Address_Type',"shipping")
    address_id=request.POST.get("Address-id")

    request.session[address_type+"_address_id"]=address_id


    next_ = request.GET.get("next")
    next_post = request.POST.get("next")
    redirected_path = next_ or next_post or None
    if is_safe_url(redirected_path, request.get_host()):
            return redirect(redirected_path)

    return redirect("/")
