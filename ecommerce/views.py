from django.contrib.auth import authenticate , login , get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render,get_object_or_404,redirect
from .forms import Contact_form,login_page,Register_page,GuestForm,Register_Form
from django.utils.http import is_safe_url
from Guest.models import Guest
from django.http import JsonResponse,HttpResponse
from django.urls import reverse
from Guest.signals import User_logged_in
from django.views.generic import CreateView,FormView,DetailView
from ecommerce.mixins import NextUrlMixin,RequestformattachMixin
from django.contrib.messages.views import SuccessMessageMixin


def home_page(request):
    context={
    "koko":"home page",
    'login_form':login_page(request.POST or None)
    }
    return render(request,"home.html",context)

def about_page(request):
    context = {
        "template_name": "About us"
    }
    return render(request,"about.html",context)

def FAQ(request):
    context = {
        "template_name": "Frequently Asked Questions (FAQ)"
    }
    return render(request,"FAQ.html",context)


def contact_page(request):
    contact_form = Contact_form(request.POST or None)
    context = {

        "form": contact_form,
        "title":"Contact Page"
    }
    if contact_form.is_valid():
        print(contact_form.cleaned_data)
        if request.is_ajax():
            print("came from ajax")
            return JsonResponse({"message":"Thank you for contacting !!"})

    if contact_form.errors:
        #print(contact_form.cleaned_data)
        errors=contact_form.errors.as_json()
        print(errors)
        if request.is_ajax():
            print("came from ajax")
            return HttpResponse(errors,status=400,content_type="application/json")

    # print(request.POST.get("fullname"))
    return render(request,"contact.html",context)

class GuestView(NextUrlMixin,FormView):
    form_class = GuestForm
    # success_url = '/register'
    # template_name = ''

    # def get_success_url(self):    # if the form is valid then will be directed to success_url from here
    #     return self.get_next_url()

    def form_valid(self, form):
        # print(form.cleaned_data)
        # next_url = self.get_next_url()
        email = form.cleaned_data.get("email",None)
        if email is not None:
            Guest_obj = Guest.objects.create(email=email)
            self.request.session["guest_id"] = Guest_obj.id
        return redirect(self.get_next_url())

    def form_invalid(self, form):
        print("why invalid !!")
        print(form.errors)
        return redirect("/register")






# def guestfnc(request):
#     guestform = GuestForm(request.POST or None)
#     context = {
#         "form": guestform
#     }
#     if guestform.is_valid():
#         print(guestform.cleaned_data)
#         email = request.POST.get("email")
#
#
#         next_ = request.GET.get("next")
#         next_post = request.POST.get("next")
#         redirected_path = next_ or next_post or None
#
#         if email is not None:
#             Guest_obj=Guest.objects.create(email=email)
#             request.session["guest_id"]=Guest_obj.id
#
#             if is_safe_url(redirected_path, request.get_host()):
#                 return redirect(redirected_path)
#             return redirect("/register")
#         else:
#             print("Error")
#
#     return redirect("/register")

class LoginView(NextUrlMixin,FormView):

    form_class = login_page
    template_name = 'login.html'

    def get_success_url(self):
        # return reverse('home')
        return self.get_next_url()


    def get_form_kwargs(self,*args,**kwargs):

        kwargs=super().get_form_kwargs(*args,**kwargs)
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):

        if self.request.method == 'POST':       # in case the checkout scenario and the user logged in
            return  redirect(self.get_next_url())
        else:
            return JsonResponse({                # in case of user logged in from the home page
                "case":'valid',
                'to_page':self.get_success_url()
            })


    def form_invalid(self, form):

        print(form.errors)
        # print(form.non_field_errors())  # errors generated from clean() function
        # print(form['Email'].errors)    # errors generated from clean_Email() function
        return JsonResponse({
            'case':'invalid',
            'errors': form.errors,

        })






# def LoginView(request):
#     login_form = login_page(request.POST or None)
#
#
#     if login_form.is_valid():
#
#         if request.is_ajax():
#             print(login_form.cleaned_data)
#             Email = request.POST.get('Email',None)
#             Password = request.POST.get('Password',None)
#             user = authenticate(email=Email, password=Password)
#             print("user=", user)
#             print(login_form.cleaned_data)
#             if user is not None:
#                 login(request, user)
#                 return redirect("/")
#             else:
#                 return redirect("/login")
#
#     return render(request,'login.html',{})

# class LoginView(NextUrlMixin,RequestformattachMixin,FormView):
#     form_class = login_page
#     template_name = 'login.html'
#     # template_name = 'home.html'
#     success_url = '/'



    #i have made mixin as it will be used in several other classes
    # we will add this form to change the handle the login page from forms perspectve not from views perspectivie
    # def get_form_kwargs(self):    # we have write this funtion to pass the request to the form to be able to read the users i/ps
    #     kwargs=super().get_form_kwargs()
    #     # kwargs={
    #     #     'request':self.request
    #     # }
    #
    #     kwargs['request']=self.request
    #     print(kwargs)
    #     return kwargs


    # i have made mixin as it will be used in several classes/modules
    # def get_next_url(self):
    #     next_ = self.request.GET.get("next")
    #     next_post = self.request.POST.get("next")
    #     redirected_path = next_ or next_post or None
    #     if is_safe_url(redirected_path, self.request.get_host()):
    #         return redirected_path     # we changed the return to be the path only
    #     return "/"


    # def form_valid(self, form):
        # request=self.request

        # print(login_form.cleaned_data)
        # username = request.POST.get("Username")                   #have changed the Username to email

        #we have commented the comming lines to change the login function from views perspectivie to form perscpective

        # email = request.POST.get("email")
        # password = request.POST.get("Password")
        # user = authenticate(username=email, password=password)
        # next_ = request.GET.get("next")
        # next_post = request.POST.get("next")
        # redirected_path = next_ or next_post or None
        # if user is not None:
        #     if not user.is_active:
        #         return super(LoginView, self).form_invalid(form)
            # User_logged_in.send(user.__class__, instance=user, request=request)
            # login(request, user)
            # if request.session.get("guest_id"):
            #     del request.session['guest_id']
            # if is_safe_url(redirected_path, request.get_host()):
            #     return redirect(redirected_path)
            # return redirect("/")

        # the following lines are the new form_valid() function
        # user = form.user  # attached user attribute from forms -- self.user=user
        # if user.is_authenticated:             # we have assure that the user is authenticated in the forms.py
        # next_url=self.get_next_url()      #we change the next url to function
        # return redirect(next_url)
        # else:
        #     print("Error")
        # return super(LoginView,self).form_invalid(form)

    # no need to to overrride the form_invalid()
    # def form_invalid(self, form):    # if the form is invalid rener the invalid form
    #     # print('mo salah')
    #     return super().form_invalid(form)
        # return redirect('/register')


# def loginfn(request):
#     login_form = login_page(request.POST or None)
#     context = {
#         "form": login_form
#     }
#     if login_form.is_valid():
#         print(login_form.cleaned_data)
#         username = request.POST.get("Username")
#         password = request.POST.get("Password")
#         user = authenticate(username=username, password=password)
#         next_=request.GET.get("next")
#         next_post=request.POST.get("next")
#         redirected_path=next_ or next_post or None
#         if user is not None:
#             User_logged_in.send(user.__class__,instance=user,request=request)
#             login(request,user)
#             if request.session.get("guest_id"):
#                 del request.session['guest_id']
#             if is_safe_url(redirected_path,request.get_host()) :
#                 return redirect(redirected_path)
#             return redirect("/")
#         else:
#             print("Error")
#     return render(request,"login.html",context)

def logout(request):
    login_form = login_page(request.POST or None)
    context = {
        "form": login_form
    }
    if login_form.is_valid():
        print(login_form.cleaned_data)
        username = request.POST.get("Username")
        password = request.POST.get("Password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect("/")
        else:
            print("Error")
    return render(request,"login.html",context)

user=get_user_model()


class RegisterView(SuccessMessageMixin,CreateView):
    form_class = Register_Form            #this will use customized save() function this is equivalent to Register_form.save()
    template_name = 'register.html'
    success_url = '/'
    success_message = '%(FirstName)s your profile has been created successfully'

    def get_form_kwargs(self,*args,**kwargs):
        kwargs=super().get_form_kwargs(*args,**kwargs)
        kwargs['request']=self.request
        return kwargs


    def form_invalid(self, form):
        return super().form_invalid(form)
# def register(request):
#     # Register_form = Register_page(request.POST or None)
#     Register_form=Register_Form(request.POST or None)
#     context = {
#         "form": Register_form
#     }
#
#     if Register_form.is_valid():
#         print(Register_form.cleaned_data)
#         Full_name = request.POST.get("full_name")
#         password = request.POST.get("password1")
#         print("password="+password)
#         email = request.POST.get("email")
#         us=user.objects.create_user(email,Full_name,password)
#         print(us)
#         # Register_form.save()  #can use the function customized function save in Register_Form Modelform
#     return render(request,"register.html",context)


@login_required                               #automatic redirect to /account/login/?next=/
def account_home_view(request):
    return render(request,'home.html',{})

# class LoginRequiredMixin(object):
    # @method_decorator(login_required)    # same as login_required for function based view but here we used @method_decorator as CBV
    # def dispatch(self, request, *args, **kwargs):
    #     return super(AccountHomeView,self).dispatch(self, request, *args, **kwargs)
    # we have transfered the above function form the below class to the above class to put ot seperatelly
    #then we but class name AccountHomeView(LoginRequiredMixin,DetailView), django already has it's LoginRequiredMixin so that class will be commented





class AccountHomeView(LoginRequiredMixin,DetailView):
    template_name = 'Accounts/home.html'
    # pass
    def get_object(self,*args,**kwargs):
        # print(self)
        return self.request.user

    # @method_decorator(login_required)    # same as login_required for function based view but here we used @method_decorator as CBV
    # def dispatch(self, request, *args, **kwargs):
    #     return super(AccountHomeView,self).dispatch(self, request, *args, **kwargs)




