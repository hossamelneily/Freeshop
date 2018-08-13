from django.shortcuts import render , get_object_or_404 ,Http404
from django.views.generic import ListView,DetailView


from products.models import product



class SearchProductView(ListView):
    template_name = "product/products.html"

    # qs_color, qs_size = None
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()

        context['colors'] = self.qs_color
        context['sizes'] = self.qs_size
        # print('colorssssssssssssss'+str(context['colors']))

        # for var in context['colors']:
        #     print(var[0])
        return context

    def get_queryset(self, *args,**kwargs):
        request=self.request
        #print(request.GET.get('q'),")
        q=request.GET.get('q',None)
        Type=request.GET.get('type',None)
        SubType=request.GET.get('subtype',None)
        # print(request.GET)
        if q is not None:
            # lookups=Q(Name__icontains=q) | Q(description__icontains=q)
            qs, self.qs_color, self.qs_size = product.objects.search(q,Type,SubType)
            return qs

        else:
            return product.objects.none()