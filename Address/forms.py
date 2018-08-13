from django import forms
from .models import Address
from billing.models import billing

class AdressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = [

            # 'billing',
            # 'Address_Type',
            'FullName',
            'ContactNo',
            'Address_line_1',
            'Address_line_2',
            'State',
            'Postal_Code',
            'city'

        ]

        widgets = {
            'FullName': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name','id':'confirmation-name-btn'}),
            'ContactNo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Phone Number','id':'confirmation-contact-btn'}),
            'Address_line_1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Address','id':'confirmation-add-btn1'}),
            'Address_line_2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Address','id':'confirmation-add-btn2'}),
            'State': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your State','id':'confirmation-add-btn3'}),
            'Postal_Code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Postal Code','id':'confirmation-add-btn4'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your city','id':'confirmation-city-btn'}),


        }

    def __init__(self,*args,**kwargs):
        self.request= kwargs.pop('request',None)
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args,**kwargs)



    def save(self, commit=True):
        request = self.request
        address = super(AdressForm,self).save(commit=False)
        # print(address)
        # print(self.cleaned_data)
        billing_profile = billing.objects.get_or_new(request)
        FullName = self.cleaned_data.get('FullName',None)
        address_type=request.POST.get('address_type',None)
        if address_type is not None:
            address.Address_Type= address_type
        if billing_profile is not None:
            address.billing = billing_profile
            # request.session[address_type + "_address_id"] = address.id
            address.FullName=FullName
        # print(self.cleaned_data)
        if commit:
            address.save()
            request.session[address_type + "_address_id"] = address.id
        return address



class UsePrevAdd(forms.ModelForm):


    class Meta:
        model=Address
        fields=('Address_Type',)

        widgets = {
            'Address_Type':forms.HiddenInput(attrs={'name':'Address_Type'})
        }