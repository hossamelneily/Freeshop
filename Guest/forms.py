from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User
from Guest.models import EmailActivaion
from django.utils.html import mark_safe
from django.urls import reverse

class EmailReactivation(forms.Form):
    email = forms.EmailField(label='Email Address')


    def clean_email(self):
        email=self.cleaned_data.get('email')
        qs = EmailActivaion.objects.filter(email__iexact=email)


        qs_active=qs.check_active()
        if not qs.exists():
            # obj=qs.first()
            # obj.Send_Activation_Email()
            register_link = reverse('register')
            msg = '''This email doesn't exists , would you like to <a href='{link}'>Register?</a>
                                '''.format(link=register_link)
            raise forms.ValidationError(mark_safe(msg))
        # else:
        #     msg = ''' This email doesn't exists , would you like to <a href='{link}'>Register?</a>
        #                                     '''.format(link=reverse('register'))
        #     raise forms.ValidationError(mark_safe(msg))

        elif qs_active.exists():
            login_link=reverse('login')
            msg='''
                This email exists and already activated , please login from here <a href='{link}'>Login</a>
            '''.format(link=login_link)
            raise forms.ValidationError(mark_safe(msg))
        return email

class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email','FirstName','LastName')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email','FirstName','LastName', 'password', 'is_active', 'admin','gender')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]