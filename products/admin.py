from django.contrib import admin
from.models import product,ProductColor,ProductSize,ProductColorSize




class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__','slug']
    class Meta:
        model = product
admin.site.register(product,ProductAdmin)
# Register your models here.


class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'product']
    class Meta:
        model = ProductSize


class ProductColorAdmin(admin.ModelAdmin):
    list_display = ['__str__','product']

    class Meta:
        model = ProductColor


class ProductSizeColor(admin.ModelAdmin):
    list_display = ['__str__','color','size']

    class Meta:
        model = ProductColorSize

admin.site.register(ProductColor,ProductColorAdmin)
admin.site.register(ProductSize,ProductSizeAdmin)
admin.site.register(ProductColorSize,ProductSizeColor)