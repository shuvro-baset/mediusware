from django.shortcuts import render
from django.views import generic
from django.views.generic import ListView, CreateView, UpdateView

from product.models import Variant, Product, ProductImage


class BaseProductView(generic.View):
    model = Product
    template_name = 'product/list.html'


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        products = Product.objects.all()
        print(products)
        context['products'] = products
        context['variants'] = list(variants.all())
        print(variants)
        return context

    def post(self, request, *args, **kwargs):
        # saving product
        product_tile = request.POST.get('product_tile')
        product_sku = request.POST.get('product_sku')
        product_desc = request.POST.get('product_desc')
        product_img = request.POST.get('product_img')
        product_ins = Product(title=product_tile, sku=product_sku, description=product_desc)
        product_ins.save()
        print(product_tile, product_sku, product_desc, product_img)
        print(product_ins)

        product_image_ins = ProductImage(product=product_ins, file_path=product_img)
        product_image_ins.save()
        print(product_image_ins)

        return render(request, 'products/create.html')


class ProductView(BaseProductView, ListView):
    template_name = 'product/list.html'

    # paginate_by = 10

    def get_queryset(self):
        filter_string = {}
        print(self.request.GET)
        for key in self.request.GET:
            if self.request.GET.get(key):
                filter_string[key] = self.request.GET.get(key)
        return Product.objects.filter(**filter_string)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = True
        context['request'] = ''
        if self.request.GET:
            context['request'] = self.request.GET['title__icontains']
        return context
