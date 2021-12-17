from django.shortcuts import render
from django.views import generic
from django.views.generic import ListView, CreateView, UpdateView

from product.models import Variant, Product, ProductImage, ProductVariantPrice


class BaseProductView(generic.View):
    model = Product
    template_name = 'products/list.html'


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context



class ProductsView(generic.TemplateView):
    template_name = 'products/list.html'

    def get(self, request):
        products = ProductVariantPrice.objects.all()
        print("products: ", products)
        context = {
            'products': products
        }
        return render(request, self.template_name, context=context)