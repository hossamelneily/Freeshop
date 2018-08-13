from django import forms
from .models import MarketingPreference


class MarketingPreferencesForm(forms.ModelForm):

    subscribed=forms.BooleanField(label="Receive marketing email?",required=False)
    class Meta:
        model = MarketingPreference
        fields = [
            'subscribed',
        ]
