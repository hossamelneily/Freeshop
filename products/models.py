from django.db import models
from django.urls import reverse
import random,os
from django.db.models import Q
from django.db.models.signals import pre_save,post_save
from .utils import unique_slug_generator
# from Tag.models import ProductColorSize
# from Tag.models import tags
from itertools import chain
# Create your models here.

def get_file_ext(filepath):
    name,ext=os.path.splitext(os.path.basename(filepath))
    return name,ext

def upload_file_name(instance,filename):
    #print(instance)
    #print(filename)
    new_file_name = random.randint(0,33763786)
    name,ext=get_file_ext(filename)
    final_file_name='{new_file_name}{ext}'.format(new_file_name=new_file_name,ext=ext)
    return "product/{new_file_name}/{final_file_name}".format(new_file_name=new_file_name,final_file_name=final_file_name)





class ProductQueryset(models.query.QuerySet):



    def featured(self):
        return self.filter(featured=True,active=True)

    def search(self,q,type=None,subtype=None):

        lookups = Q(Name__icontains=q) | Q(description__icontains=q) | Q(tags__slug__icontains=q)
        # print(q)
        if type is not None and subtype is not None and q is not None:


            if type == 'all':
                qs = self.filter(lookups).distinct()
                qs_color = product().Search_for_colors_in_ProductColorTable(qs)
                qs_size = product().Search_for_sizes_in_ProductSizeTable(qs)
                return qs ,qs_color , qs_size
            if type == 'Mens':
                qs= self.men_clothes()
            elif type == 'Womens':
                qs=self.women_clothes()
            elif type =='kids':
                qs=self.kids_clothes()
            elif type == 'Technology':
                qs=self.electronics()
            elif type == 'home&style':
                qs=self.home_style()
            else:
                qs=self.sports()
            qs_color = product().Search_for_colors_in_ProductColorTable(qs)
            qs_size = product().Search_for_sizes_in_ProductSizeTable(qs)
            return qs.filter(tags__SubType__icontains=subtype).filter(lookups),qs_color,qs_size
        qs=self.filter(lookups).distinct()
        qs_color = product().Search_for_colors_in_ProductColorTable(qs)
        qs_size = product().Search_for_sizes_in_ProductSizeTable(qs)
        return qs,qs_color,qs_size  # in case choose category= all and don't type search values , in that case there will not be type and subtype there will be category

    def active(self):
        return self.filter(active=True)

    def men_clothes(self):
        return self.filter(tags__Type='menclothes').distinct()

    def women_clothes(self):
        return self.filter(tags__Type='womenclothes').distinct()


    def kids_clothes(self):
        return self.filter(tags__Type='kidsclothes').distinct()

    def electronics(self):
        return self.filter(tags__Type='electronics').distinct()

    def home_style(self):
        return self.filter(tags__Type='home&lifestyle').distinct()

    def sports(self):
        return self.filter(tags__Type='sports').distinct()

    def SubTypes(self,subtype):
        return self.filter(tags__SubType=subtype)


    # def Filter_brand(self,brands):
    #     brands_split = brands.split(',')
    #     if len(brands_split)>0:
    #         q_objects=Q()
    #         for item in brands_split:
    #             q_objects.add(Q(tags__Brand=item),Q.OR)
    #         qs = self.filter(q_objects).distinct()
    #         qs_color = product().Search_for_colors_in_ProductColorTable(qs)
    #         qs_size = product().Search_for_sizes_in_ProductSizeTable(qs)
    #     return  qs,qs_color,qs_size
    #
    # def Filter_size(self,sizes):
    #     sizes_split = sizes.split(',')
    #     if len(sizes_split)>0:
    #         q_objects=Q()
    #         for item in sizes_split:
    #             q_objects.add(Q(productsize__size=item),Q.OR)
    #         qs = self.filter(q_objects).distinct()
    #         qs_color = product().Search_for_colors_in_ProductColorTable(qs)
    #         qs_size = product().Search_for_sizes_in_ProductSizeTable(qs)
    #     return  qs,qs_color,qs_size
    #
    # def Filter_color(self, colors):
    #     colors_split = colors.split(',')
    #     if len(colors_split) > 0:
    #         q_objects = Q()
    #         for item in colors_split:
    #             q_objects.add(Q(productcolor__color=item), Q.OR)
    #         qs = self.filter(q_objects).distinct()
    #         qs_color = product().Search_for_colors_in_ProductColorTable(qs)
    #         qs_size = product().Search_for_sizes_in_ProductSizeTable(qs)
    #     return qs, qs_color, qs_size
    #
    # def Filter_Price(self,PriceFrom,PriceTo):
    #
    #     if PriceFrom and PriceTo:
    #         lookup = Q(price__gte=PriceFrom) & Q(price__lte=PriceTo)
    #
    #     elif PriceFrom and not PriceTo:
    #         lookup = Q(price__gte=PriceFrom)
    #     elif PriceTo and not PriceFrom:
    #         lookup=Q(price__lte=PriceTo)
    #
    #     qs = self.filter(lookup).distinct()
    #     qs_color = product().Search_for_colors_in_ProductColorTable(qs)
    #     qs_size = product().Search_for_sizes_in_ProductSizeTable(qs)
    #
    #     return qs, qs_color, qs_size

    def Filter_by(self,brands,sizes,colors,PriceFrom,PriceTo):
        brands_split = brands.split(',')
        sizes_split = sizes.split(',')
        colors_split = colors.split(',')
        qs = product.objects.none()
        filter_by_price =False
        # print(type(PriceFrom))
        if len(brands_split) > 0:
            q_objects = Q()
            for item in brands_split:
                q_objects.add(Q(tags__Brand=item), Q.OR)
            qs = self.filter(q_objects).distinct()


        if len(sizes_split) > 0:
            q_objects = Q()
            for item in sizes_split:
                q_objects.add(Q(productsize__size=item), Q.OR)
            qs = qs | self.filter(q_objects).distinct()


        if len(colors_split) > 0:
            q_objects = Q()
            for item in colors_split:
                q_objects.add(Q(productcolor__color=item), Q.OR)
            qs = qs | self.filter(q_objects).distinct()

        if PriceFrom and PriceTo:
            # print("price")
            filter_by_price =True
            lookup = Q(price__gte=PriceFrom) & Q(price__lte=PriceTo)

        elif PriceFrom and not PriceTo:
            # print("price")
            filter_by_price = True
            lookup = Q(price__gte=PriceFrom)
        elif PriceTo and not PriceFrom:
            # print("price")
            filter_by_price = True
            lookup = Q(price__lte=PriceTo)

        if filter_by_price:
            qs = qs | self.filter(lookup).distinct()

        qs = qs.distinct()
        qs_color = product().Search_for_colors_in_ProductColorTable(qs)
        qs_size = product().Search_for_sizes_in_ProductSizeTable(qs)
        return qs,qs_color,qs_size




class ProductManager(models.Manager):
    def get_by_id(self,id):
        return self.get_queryset().filter(id=id).first()     #product.objects == self.get_queryset()
                                                             #self.get_queryset().filter(id=id) will return queryset
                                                             #self.get_queryset().filter(id=id).first() return instance

    def get_by_slug(self,slug):
        return self.get_queryset().filter(slug=slug).first()


    def get_by_category(self,category):


        if category == 'menclothes':
            qs = self.get_queryset().active().men_clothes()

        elif category == 'womenclothes':
            qs = self.get_queryset().active().women_clothes()

        elif category == 'Kidsclothes':
            qs = self.get_queryset().active().kids_clothes()

        elif category == 'electronics':
            qs = self.get_queryset().active().electronics()

        elif category == 'HomeStyle':
            qs = self.get_queryset().active().home_style()

        elif category == 'sports':
            qs = self.get_queryset().active().sports()



        if qs.exists():
            qs_color = product().Search_for_colors_in_ProductColorTable(qs)
            qs_size = product().Search_for_sizes_in_ProductSizeTable(qs)

            return qs,qs_color,qs_size
        else:
            qs = product.objects.none()
            qs_color = ProductColor.objects.none()
            qs_size = ProductSize.objects.none()
            return qs,qs_color,qs_size


    def featured(self):
        return self.get_queryset().filter(featured=True)

    def all(self):
        return self.get_queryset().filter(active=True)

    def get_queryset(self):
        return ProductQueryset(self.model,using=self._db)

    def search(self,q,type,subtype):                                     #products.objects.search(q)

        #return product.objects.filter(lookups).distinct()
        #return self.get_queryset().featured().search(q)     #means featured and from featured products will search for
        return self.get_queryset().active().search(q,type,subtype)


    def Filter_by(self,brands,sizes,colors,pricefrom,priceto):
        return self.get_queryset().Filter_by(brands,sizes,colors,pricefrom,priceto)

    # def Filter_brand(self,brands):
    #     return self.get_queryset().Filter_brand(brands)
    #
    # def Filter_size(self,sizes):
    #     return self.get_queryset().Filter_size(sizes)
    #
    # def Filter_color(self,colors):
    #     return self.get_queryset().Filter_color(colors)
    #
    # def Filter_price(self,pricefrom,priceto):
    #     return self.get_queryset().Filter_Price(pricefrom,priceto)
    #
    # def Filter_Brand_Size(self,brands,sizes):
    #     return self.get_queryset().Filter_brand(brands)[0].Filter_size(sizes)
    #
    # def Filter_Brand_Size_color(self,brands,sizes,colors):
    #     return self.get_queryset().Filter_brand(brands)[0].Filter_size(sizes)[0].Filter_color(colors)
    #
    # def Filter_Brand_color(self,brands,colors):
    #     return self.get_queryset().Filter_brand(brands)[0].Filter_color(colors)
    #
    # def Filter_Size_color(self,sizes,colors):
    #     return self.get_queryset().Filter_size(sizes)[0].Filter_color(colors)
    #
    #
    # def Filter_Brand_Size_Price(self,brands,sizes,pricefrom,priceto):
    #     return self.get_queryset().Filter_brand(brands)[0].Filter_size(sizes)[0].Filter_Price(pricefrom,priceto)
    # def Filter_Brand_Size_color_price(self,brands,sizes,colors,pricefrom,priceto):
    #     return self.get_queryset().Filter_brand(brands)[0].Filter_size(sizes)[0].Filter_color(colors)[0].Filter_Price(pricefrom,priceto)
    # def Filter_Brand_color_price(self,brands,colors,pricefrom,priceto):
    #     return self.get_queryset().Filter_brand(brands)[0].Filter_color(colors)[0].Filter_Price(pricefrom,priceto)
    # def Filter_Size_color_price(self,sizes,colors,pricefrom,priceto):
    #     return self.get_queryset().Filter_size(sizes)[0].Filter_color(colors)[0].Filter_Price(pricefrom,priceto)
    # def Filter_brand_price(self,brands,pricefrom,priceto):
    #     return self.get_queryset().Filter_brand(brands)[0].Filter_Price(pricefrom,priceto)
    # def Filter_size_price(self,sizes,pricefrom,priceto):
    #     return self.get_queryset().Filter_size(sizes)[0].Filter_Price(pricefrom,priceto)
    # def Filter_color_price(self,colors,pricefrom,priceto):
    #     return self.get_queryset().Filter_color(colors)[0].Filter_Price(pricefrom,priceto)
COLOR=(
    ('white','White'),
    ('red','Red'),
    ('black','Black'),
    ('blue','Blue'),
    ('yellow','Yellow'),
    ('green','Green'),
    ('purple','Purple'),
    ('orange','Orange'),
    ('pink','Pink'),
)

SIZE = (
('Extra Small', 'XS'),  #(DB,Display)
('Small', 'S'),
('Medium', 'M'),
('Small Medium', 'sm'),
('Large', 'L'),
('Extra Large', 'XL'),
('Double Large', 'XXL'),
('Triple Large', 'XXXL'),
('13 inch', '13 \'\''),
('15 inch', '15 \'\'')
)

class product(models.Model):
    Name                     = models.CharField(max_length=250)  #hossam shorts
    slug                     = models.SlugField(blank=True,unique=True)
    description              = models.CharField(max_length=1000,blank=False)
    price                    = models.DecimalField(decimal_places=2,max_digits=20,default=39.99,blank=False)
    image                    = models.ImageField(upload_to=upload_file_name,null=True,blank=True)
    img1                     = models.ImageField(upload_to=upload_file_name, null=True, blank=True)
    img2                     = models.ImageField(upload_to=upload_file_name, null=True, blank=True)
    img3                     = models.ImageField(upload_to=upload_file_name, null=True, blank=True)
    img4                     = models.ImageField(upload_to=upload_file_name, null=True, blank=True)
    featured                 = models.BooleanField(default=False)                                  # favourite products
    active                   = models.BooleanField(default=True)
    timestamp                = models.DateTimeField(auto_now_add=True,editable=True)

    objects=ProductManager()


    def __str__(self):
        return self.Name


    def get_absolute_url(self):
        #return "{slug}".format(slug=self.slug)
        # ps = reverse("product:category")

        return reverse("products:detail",kwargs={"slug":self.slug})

    def classify_types(self,type):
        switcher = {
            'Mens': "men_clothes()",
            'Womens': "women_clothes()",
            'kids': "kids_clothes()",
            'Technology': "electronics()",
            'home&style': "home_style()",
            'Sportwear': "sports()"

        }
        return switcher.get(type,None)

    def Search_for_colors_in_ProductColorTable(self, qs):
        qs__color = ProductColor.objects.none()
        for qs_instance in qs:
            qs_color = ProductColor.objects.filter(product__Name=qs_instance.Name).values_list('product__Name','color').distinct()
            # print(qs_color)
            qs__color = qs__color | qs_color
        # print(qs__color)
        return qs__color

    def Search_for_sizes_in_ProductSizeTable(self,qs):
        qs__size = ProductSize.objects.none()
        for qs_instance in qs:
            qs_size = ProductSize.objects.filter(product__Name=qs_instance.Name).values_list('product__Name','size').distinct()
            qs__size = qs__size | qs_size
        return qs__size

class ProductSize(models.Model):
    product      = models.ForeignKey(product,on_delete=models.CASCADE)
    # tag          =models.ForeignKey(tags,on_delete=models.CASCADE)
    size         = models.CharField(max_length=100,blank=False,default='Small',choices=SIZE)
    sale_price   = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)
    active       = models.BooleanField(default=True)

    def __str__(self):      #need to change it to size
        return self.size

class ProductColor(models.Model):
    product         = models.ForeignKey(product,on_delete=models.CASCADE)
    # tag             = models.ForeignKey(tags,on_delete=models.CASCADE)
    color           = models.CharField(default='white',max_length=100,blank=True,choices=COLOR)
    active          = models.BooleanField(default=True)

    def __str__(self):   # need to change to color
        return self.color


class ProductColorSize(models.Model):
    product        = models.ForeignKey(product,on_delete=models.CASCADE)
    # tag            = models.ForeignKey(tags,on_delete=models.CASCADE)
    color          = models.ForeignKey(ProductColor,blank=True,null=True,on_delete=models.CASCADE)
    size           = models.ForeignKey(ProductSize,blank=True,null=True,on_delete=models.CASCADE)


    def __str__(self):
        return "{product},{color},{size}".format(product=self.product.Name,color=self.color,size=self.size)
def product_Color_postsave(sender,created,instance,*args,**kwargs):
    if created and instance.Name:
        ProductColor.objects.create(product=instance)
        # need to add Color

post_save.connect(product_Color_postsave,sender=product)

def product_Size_postsave(sender,created,instance,*args,**kwargs):
    if created and instance.Name:
        ProductSize.objects.create(product=instance)
        # need to add Size

post_save.connect(product_Size_postsave,sender=product)


def product_Color_Size_postsave(sender,created,instance,*args,**kwargs):
    if created and instance.Name:
        ProductColorSize.objects.create(product=instance)
        # need to add size and color

post_save.connect(product_Color_Size_postsave,sender=product)



# product  slug
def product_presave(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_presave,sender=product)




