from django.contrib import admin

# Register your models here.
from .models import billing,Card,Charge


admin.site.register(Charge)
admin.site.register(Card)
admin.site.register(billing)
