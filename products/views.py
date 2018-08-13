from django.shortcuts import render , get_object_or_404 ,Http404
from django.views.generic import ListView,DetailView
from cart.models import cart
from .models import product,ProductSize,ProductColorSize
from Analytic.Mixin import ObjectMixinView
from django.shortcuts import render_to_response
from django.http import JsonResponse


class ProductlistView(ListView):
    #queryset=product.objects.all()
    model = product
    template_name = "product/product.html"

    def get_context_data(self, *args, **kwargs):
        context=super(ProductlistView,self).get_context_data(*args,**kwargs)
        context['cart']=cart.objects.get_or_create(self.request)
        # print(context)
        return context

    def get_queryset(self, *args,**kwargs):
        return product.objects.all()


class FeaturedProductlistView(ListView):                          #featured products
    template_name = "product/product.html"
    def get_queryset(self):
        return product.objects.featured()


class FeaturedProductlistView(ListView):                          #featured products
    template_name = "product/product.html"
    def get_queryset(self):
        return product.objects.featured()







class MainProductlistView(ListView):

    template_name = 'product/products.html'

    # qs_color, qs_size = None
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()

        context['colors'] = self.qs_color
        context['sizes'] = self.qs_size
        context['cart'] = cart.objects.get_or_create(self.request)
        # print('colorssssssssssssss'+str(context['colors']))

        # for var in context['colors']:
        #     print(var[0])
        return context


    def get_queryset(self,*args,**kwargs):
        category = self.kwargs.get('category',None)
        # print(kwargs)
        if category is not None:
            qs,self.qs_color,self.qs_size = product.objects.get_by_category(category)
        else:
            # if the user entered invalid url
            qs = product.objects.none()
        return qs











class FeaturedProductDetailView(DetailView):                     #featured products Details view
    #queryset = product.objects.all()
    template_name = "product/detail.html"

    def get_queryset(self, *args,**kwargs):
        pk=self.kwargs.get("pk")
        return product.objects.featured()



class ProductDetailSlugView(ObjectMixinView,DetailView):
    # queryset = product.objects.all()
    template_name = "product/productDetails.html"
    # print(queryset)

    # def get_context_data(self, *args,**kwargs):
    #     context=super(productdetailview,self).get_context_data(*args,**kwargs)
    #     print(context)
    #     print(self.kwargs.get("pk"))
    #     return context
    def classify_types(self,size,color,context):


        switcher = {
            'Extra Small': 'xs',
            'Small': 's',
            'Medium': 'm' ,
            'Small Medium': 'sm',
            'Large': 'l',
            'Extra Large': 'xl',
            'Double Large': 'xxl',
            'Triple Large': 'xxxl',
            '13 inch': '13inch',
            '15 inch': '15inch'

        }
        # x= switcher.get(size,None)
        # print("switcher"+str(switcher.get(size,None)))
        context[switcher.get(size, None)].append(color)
        # context[switcher.get(size, None)]= x
        # print(x)



    def get_context_data(self, *args, **kwargs):
        qs__size__color = ProductColorSize.objects.none()
        context=super(ProductDetailSlugView,self).get_context_data(*args,**kwargs)
        context['xs'],context['s'],context['m'],context['sm'], \
        context['l'],context['xl'],context['xxl'], \
        context['xxxl'],context['13inch'],context['15inch'] = ([] for i in range(10))
        context['cart']=cart.objects.get_or_create(self.request)
        product_obj    =product.objects.get_by_slug(self.kwargs.get("slug"))
        if product_obj:
            qs_sizes  = ProductSize.objects.filter(product__Name=product_obj.Name).values_list('size').distinct()
            context['qs_sizes'] = qs_sizes
            if qs_sizes.exists:
                for size_obj in qs_sizes:
                    qs_SizeColor = ProductColorSize.objects.filter(product__Name=product_obj.Name,size__size=size_obj[0]).values_list('size__size','color__color').distinct()
                    qs__size__color = qs__size__color | qs_SizeColor
                    context['qs__size__color']=qs__size__color

                for size_color in qs__size__color:
                    # print(size_color[0])
                    self.classify_types(size_color[0],size_color[1],context)
        # print(context)
        return context

    def get_object(self, *args,**kwargs):
        # print(args)
        # print(kwargs)
        # pk=self.kwargs.get("pk")
        # slug=
        # print(self.kwargs.get("slug"))
        # print(product.objects.get_by_slug(self.kwargs.get("slug")))
        return product.objects.get_by_slug(self.kwargs.get("slug"))



class productdetailview(DetailView):
    #queryset = product.objects.all()
    template_name = "product/detail.html"

    # def get_context_data(self, *args,**kwargs):
    #     context=super(productdetailview,self).get_context_data(*args,**kwargs)
    #     # print(context)
    #     print(self.kwargs.get("pk"))
    #     return context

    def get_object(self, *args,**kwargs):
        pk=self.kwargs.get("pk")
        #print(self.queryset)
        return product.objects.get_by_id(pk)


def Productfnc(request):
    qs = product.objects.all()
    context={
        "object_list":qs
    }
    return render(request,"product/product.html",context)


def detailfnc(request,album_id):
    #qs = product.objects.get(id=album_id)
    #qs=get_object_or_404(product,id=album_id)
    instance=product.objects.get_by_id(album_id)
    if instance is None:
        raise Http404("product doesn't exist!!!!!!!!")
    print(instance)
    context={
        "object":instance
    }
    return render(request,"product/detail.html",context)