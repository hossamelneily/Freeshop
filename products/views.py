from django.shortcuts import render , get_object_or_404 ,Http404
from django.views.generic import ListView,DetailView
from cart.models import cart
from .models import product,ProductSize,ProductColorSize
from Analytic.Mixin import ObjectMixinView
from django.shortcuts import render_to_response
from django.http import JsonResponse
import pickle
from django.template.loader import render_to_string

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
        ps_arr = cart.objects.get_or_create(self.request).products.all()
        # ps_arr = Cart_to_send.products.all()
        context = super().get_context_data()

        context['colors'] = self.qs_color
        context['sizes'] = self.qs_size
        context['cart'] = cart.objects.get_or_create(self.request)
        # self.request.session['ps_arr'] = pickle.dumps(ps_arr)
        # print(self.request.GET)
        # print('colorssssssssssssss'+str(context['colors']))

        # for var in context['colors']:
        #     print(var[0])
        return context


    def get_queryset(self,*args,**kwargs):
        category = self.kwargs.get('category',None)
        filter_brand = self.request.GET.get('filter_brand',None)
        filter_size = self.request.GET.get('filter_size',None)
        filter_color = self.request.GET.get('filter_color',None)
        PriceFrom = self.request.GET.get('PriceFrom',None)
        PriceTo = self.request.GET.get('PriceTo',None)

        # print(kwargs)
        if category is not None:
            self.request.session['category'] = category


            if filter_brand or filter_size or filter_color or PriceFrom or PriceTo:
                print("filterby  function!")
                # print(PriceFrom)
                # print(PriceTo)
                # print(filter_brand)
                # print(filter_size)
                # print(filter_color)

                products_qs, self.qs_color, self.qs_size = product.objects.get_by_category(category)[0].Filter_by(
                filter_brand.rstrip(','), filter_size.rstrip(','), filter_color.rstrip(','),PriceFrom,PriceTo)
                # print(products_qs)
                return products_qs

            # if filter_brand and filter_size and filter_color:
            #     print("filter brand&Size&color  function!")
            #     products_qs, self.qs_color, self.qs_size = product.objects.Filter_Brand_Size_color(filter_brand.rstrip(','),filter_size.rstrip(','),filter_color.rstrip(','))
            #     return products_qs
            #
            # elif filter_brand and filter_size:
            #     print("filter brand&Size  function!")
            #     products_qs, self.qs_color, self.qs_size = product.objects.Filter_Brand_Size(filter_brand.rstrip(','),filter_size.rstrip(','))
            #     return products_qs
            #
            #
            # elif filter_brand and filter_color:
            #     print("filter brand&Color  function!")
            #     products_qs, self.qs_color, self.qs_size = product.objects.Filter_Brand_color(filter_brand.rstrip(','),filter_color.rstrip(','))
            #     return products_qs
            #
            # elif filter_size and filter_color:
            #     print("filter Size&Color  function!")
            #     products_qs, self.qs_color, self.qs_size = product.objects.Filter_Size_color(filter_size.rstrip(','),filter_color.rstrip(','))
            #     return products_qs
            #
            #
            # elif filter_brand:
            #     print("filter brand  function!")
            #     products_qs, self.qs_color, self.qs_size = product.objects.Filter_brand(filter_brand.rstrip(','))
            #     return products_qs
            #
            # elif filter_size:
            #     print("filter size  function!")
            #     print(filter_size)
            #     products_qs, self.qs_color, self.qs_size = product.objects.Filter_size(filter_size.rstrip(','))
            #     print(products_qs)
            #     return products_qs
            #
            # elif filter_color:
            #     print("filter Color  function!")
            #     print(filter_color)
            #     products_qs, self.qs_color, self.qs_size = product.objects.Filter_color(filter_color.rstrip(','))
            #     print(products_qs)
            #     return products_qs
            #
            # if PriceFrom or PriceTo:
            #     print("filter Price  function!")


            qs,self.qs_color,self.qs_size = product.objects.get_by_category(category)
        else:
            # if the user entered invalid url
            qs = product.objects.none()
        return qs





# def Filter_Products(request):
#     context={
#        'request':request
#     }
#     if request.is_ajax():
#         if request.method == 'GET':
#             print("filter by function!")
#             filter_brand = request.GET.get('filter_brand')
#             products_qs, qs_color, qs_size = product.objects.Filter_brand(filter_brand.rstrip(','))
#
#
#
#             # request.session['object_list']=products_qs
#             # request.session['colors'] = qs_color
#             # request.session['sizes'] = qs_size
#
#
#             context['object_list'] = products_qs
#             context['colors']= qs_color
#             context['sizes']=qs_size
#             html = render_to_string('product/products.html',context)
#             # print(html)
#             # print(qs_color)
#             # print(qs_size)
#             return  JsonResponse({
#                 'html':html
#             })
#     return render(request,"product/products.html",context)



# class Filter_By_Brand(ListView):
#
#     template_name = 'product/products.html'
#
#
#     def get_queryset(self):
#         request=self.request
#         # if request.is_ajax():
#         #     if request.method == 'GET':
#         print("filter by function!")
#         filter_brand = request.GET.get('filter_brand')
#
#         products_qs, self.qs_color, self.qs_size = product.objects.Filter_brand(filter_brand.rstrip(','))
#         return products_qs
#
#     def get_context_data(self, *args, object_list=None, **kwargs):
#         context= super().get_context_data( *args, object_list=None, **kwargs)
#         context['colors'] = self.qs_color
#         context['sizes'] = self.qs_size
#         return context



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
        context[switcher.get(size, None)].append(color)



    def get_context_data(self, *args, **kwargs):
        qs__size__color = ProductColorSize.objects.none()
        context=super(ProductDetailSlugView,self).get_context_data(*args,**kwargs)
        context['xs'],context['s'],context['m'],context['sm'], \
        context['l'],context['xl'],context['xxl'], \
        context['xxxl'],context['13inch'],context['15inch'] = ([] for i in range(10))
        context['cart']=cart.objects.get_or_create(self.request)
        product_obj    =product.objects.get_by_slug(self.kwargs.get("slug"))
        # self.request.session['ps_arr']= context['ps_arr']
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
        print(context)
        return context

    def get_object(self, *args,**kwargs):
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