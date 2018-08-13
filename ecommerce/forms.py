from django import forms
from django.contrib.auth import authenticate , login , get_user_model
from Guest.signals import User_logged_in
from Guest.models import Guest
from Guest.models import EmailActivaion
from django.urls import reverse
from django.contrib import messages
from django.utils.html import mark_safe
import re

User=get_user_model()

class Contact_form(forms.Form):
        fullname=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"your Name","id":"name","name":"koko"}))
        email=forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control","placeholder":"your Email"}))
        content=forms.CharField(widget=forms.Textarea(attrs={"class":"form-control","placeholder":"your message"}))

        def clean_email(self):
            if not "gmail.com"  in  self.cleaned_data.get("email"):
                raise forms.ValidationError("The email must be @gmail.com")
            return self.cleaned_data.get("email")

        def clean_fullname(self):
            if len(self.cleaned_data.get("fullname")) < 3:
                raise forms.ValidationError("The username is too short !")
            return self.cleaned_data.get("fullname")

class login_page(forms.Form):
    Email = forms.EmailField(label='Email address',required=True,widget=forms.EmailInput(
        attrs={"class": "form-control", "placeholder": "Email address", "id": "confirmation-email-btn",'aria-describedby':'emailHelp'}))
    Password = forms.CharField(required=True,widget=forms.PasswordInput(attrs={"class": "form-control",'id':'exampleInputPassword2',
                            "placeholder": "Password"}))


    def __init__(self,*args,**kwargs):
        print(kwargs)
        self.request=kwargs.pop('request',None)
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args,**kwargs)




    def clean(self):
        email = self.cleaned_data.get('Email')
        password = self.cleaned_data.get('Password',None)

        print(email)  # will print None if it raised validationError

        if email is not None:
            qs = User.objects.filter(email=email)
            if not qs.exists():
                regirster_link = reverse('register')
                msg = '''This user is not register , please click the link to <a href='{link}'>Join Us</a>
                                                                   '''.format(link=regirster_link)
                raise forms.ValidationError(mark_safe(msg))
            user = authenticate(email=email, password=password)
            if user is not None:
                login(self.request, user)
                try:
                    del self.request.session['guest_id']
                    print("killed the guest session,as the user logged in")
                except:
                    print("this session doesn't have guest_id")
                print('user is logged')
            else:

                print("Invalid credentials")
                raise forms.ValidationError("Invalid credentials")

        return self.cleaned_data


gender=(
    ('M','Male'),
    ('F','Female')
)

class Register_Form(forms.ModelForm):
        """A form for creating new users. Includes all the required
        fields, plus a repeated password."""
        password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control','id':'password1','placeholder':'password'}),required=True)
        password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(
            attrs={'class':'form-control','id':'password2','placeholder':'password confimration'}),required=True)
        # gender   =  forms.ChoiceField(choices=gender, widget=forms.RadioSelect(attrs={'class':'form-control'}))



        class Meta:
            model = User
            fields = ('FirstName','LastName','email')

            widgets = {
                'FirstName':forms.TextInput(attrs={'class':'form-control','placeholder':'first Name'}),
                'LastName': forms.TextInput(attrs={'class':'form-control','placeholder': 'last Name'}),
                'email': forms.EmailInput(attrs={'class':'form-control','placeholder': 'email address'}),
                # 'gender':forms.RadioSelect(attrs={'class':'form-control'},choices=gender)

            }

        def __init__(self, *args, **kwargs):
            self.request = kwargs.pop('request')
            # print(kwargs)
            kwargs.setdefault('label_suffix', '')
            super().__init__(*args, **kwargs)


        def clean_email(self):
            email =self.cleaned_data.get('email')

            if email is not None:
                qs = User.objects.filter(email=email)
                if qs.exists():
                    # print("email exists")
                    reset_password_link=reverse('password_reset')
                    msg = '''Email already exists,  
                    <a href="{link}">reset your password?</a>'''.format(link=reset_password_link)
                    raise forms.ValidationError(mark_safe(msg))
            return email


        def clean_password2(self):
            # Check that the two password entries match
            password1 = self.cleaned_data.get("password1")
            password2 = self.cleaned_data.get("password2")
            if password1 and password2 and password1 != password2:
                raise forms.ValidationError("Passwords don't match")
            return password2

        def save(self,commit=True):
            request=self.request
            # Save the provided password in hashed format
            user = super().save(commit=False)
            user.set_password(self.cleaned_data["password1"])
            # user.is_active=False    #need the confirmation mail
            if (request.POST.get('gender') == 'M'):
                user.gender = 'Male'
            else:
                user.gender = 'Female'
            user.country = request.POST.get('country',None)
            print(self.cleaned_data)  # this will print only the fields of the form.forms or from.Modelform
            print(request.POST)   # this will return all the html tags/elements between from tag , even this tag/element not in the froms
            if commit:
                user.save()
            return user


class Register_page(forms.Form):
    Username = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": "your Name", "id": "name", "name": "koko"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "your Email"}))
    Password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
    Password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))


    def clean(self):
        if self.cleaned_data.get("Password1") != self.cleaned_data.get("Password2"):
            raise forms.ValidationError("The passwords must match")
        #return self.cleaned_data
    def clean_Username(self):
        #self.cleaned_data.get("Username")
        qs=User.objects.filter(username=self.cleaned_data.get("Username"))
        if qs.exists():
            raise forms.ValidationError("Username already exists")



class GuestForm(forms.Form):
    email = forms.EmailField(label='Email Address',widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter Email"}))

    # def __init__(self, *args, **kwargs):
    #     self.request=kwargs.pop('request',None)
    #     super().__init__(*args,**kwargs)



# class GuestForm(forms.ModelForm):
#     # email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "your Email"}))
#
#     class Meta:
#         model = Guest
#         fields=[
#             'email',
#         ]
#
#     def __init__(self,*args,**kwargs):
#         self.request=kwargs.pop('request',None)
#         super().__init__(*args,**kwargs)
#
#
#     def clean(self):
#         request=self.request
#         email = request.POST.get("email")
#
#         if email is not None:
#
#             Guest_obj = Guest.objects.create(email=email)
#             request.session["guest_id"] = Guest_obj.id
#         else:
#             raise forms.ValidationError("Please enter an email!")
#         print(self.cleaned_data)
#         return self.cleaned_data

    # def save(self, commit=True):
    #     # Save the provided password in hashed format
    #     obj = super().save(commit=False)
    #
    #     if commit:
    #         obj.save()
    #         self.request.session["guest_id"] = obj.id
    #     return user