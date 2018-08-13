from django.contrib import admin
from .models import MarketingPreference
# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import MarketingPreference

class Marketing_pref_admin(admin.ModelAdmin):
    list_display = ('__str__', 'subscribed','updated')
    readonly_fields = ('mailchimp_msg','timestamp','updated')

    # class Meta:    #  the video this part is added but i don't know why
    #     model=MarketingPreference
    #     fields=[
    #
    #     ]
admin.site.register(MarketingPreference,Marketing_pref_admin)