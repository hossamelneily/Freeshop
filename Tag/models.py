from django.db import models
from products.models import product
from django.db.models.signals import pre_save,post_save
from products.utils import unique_tags_slug_generator
# Create your models here.

ProductType = (

    ("menclothes","MenClothes"),
    ("womenclothes","WomenClothes"),
    ('kidsclothes','KidsClothes'),
    ('electronics','Electronics'),
    ('home&lifestyle','Home&LifeStyle'),
    ('sports','Sports')
)


ProductSubType = (

  #Men/Women/Kids/Sports
    ('shoes','Shoes'),
    ('bags','Bags'),
    ('accessories','Accessories'),
    ('clothes','Clothes'),
    ('shirts','Shirts'),
  #ELectronics
    ('mobiles','Mobiles'),
    ('cameras','Cameras'),
    ('laptop','Laptop'),

   #Home&LifeStyle
    ('tv','TV'),
    ('washingMachines','WashingMachines')




)

ProductSub_Type = (

    ('sneakers','Sneakers'),
    ('boots','Boots'),
    ('sandals','Sandals'),
    ('watches','Watches'),
    ('sunglasses','Sunglasses'),
    ('perfumes','Perfumes'),
    ('jewellery','Jewellery')

)





class tags(models.Model):
    # title        = models.CharField(max_length=123)
    # description  = models.CharField(max_length=500)
    slug         = models.SlugField(blank=True, unique=True)
    product     = models.ForeignKey(product, on_delete=models.CASCADE)

    Brand        = models.CharField(max_length=250,blank=True,null=True)
    # color         = models.ManyToManyField(Color,max_length=100,blank=True)
    # color        =models.CharField(max_length=100,blank=False,default='white',choices=color)
    # gender       = models.CharField(max_length=75,blank=True,null=True)
    Type         = models.CharField(max_length=300,blank=False,choices=ProductType)
    SubType      =models.CharField(max_length=300,blank=False,choices=ProductSubType)
    SubSubType   =models.CharField(max_length=300,blank=True,null=True,choices=ProductSub_Type)

    active = models.BooleanField(default=True)
    weight = models.CharField(max_length=100, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.slug









# def ProductSize_postsave(sender,instance,created,*args,**kwargs):
#     if created:
#         ProductSize.objects.create(product=)
def Tags_slug_presave(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug=unique_tags_slug_generator(instance)
pre_save.connect(Tags_slug_presave,sender=tags)




def product_tags_postsave(sender,created,instance,*args,**kwargs):
    if created and instance.Name:
        tags.objects.create(product=instance)
        # need to add Type,SubType, SubsubType

post_save.connect(product_tags_postsave,sender=product)