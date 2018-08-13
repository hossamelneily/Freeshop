# from django.contrib import admin
#
# # Register your models here.
from .models import Guest,EmailActivaion
# ,User
#
#
# class Admin(admin.ModelAdmin):
#     search_fields = ['email']
#
# admin.site.register(User,Admin)
#
# admin.site.register(Guest)


from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminChangeForm,UserAdminCreationForm

# from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import User

class UserAdmin(BaseUserAdmin):        #admin.ModelAdmin
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # # The fields to be used in displaying the User model.
    # # These override the definitions on the base UserAdmin
    # # that reference specific fields on auth.User.
    list_display = ('email', 'is_active','admin')
    list_filter = ('admin','staff')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal information', {'fields': ('FirstName','LastName','country','gender')}),
        ('Permissions', {'fields': ('is_active','admin','staff')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


class EmailActivation(admin.ModelAdmin):
    search_fields = ['email']

admin.site.register(User, UserAdmin)
admin.site.register(Guest)
admin.site.register(EmailActivaion,EmailActivation)

# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)

