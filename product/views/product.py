from django.shortcuts import render
from django.views import generic
from django.views.generic import ListView, CreateView, UpdateView
from django.core.paginator import Paginator
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
        # todo: pagination start
        paginator = Paginator(products, 10)
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)
        print("ad", page_obj, paginator)
        # todo: pagination end
        context = {
            # 'products': products,
            "page_obj": page_obj
        }
        return render(request, self.template_name, context=context)

    def post(self, request):
        if request.method == "POST":
            name = request.POST.get('title')
            price_from = request.POST.get('price_from')
            price_to = request.POST.get('price_to')
            print("name: ", name)
            product_ins = ProductVariantPrice.objects.all()
            products = product_ins.filter(product__title__icontains=name, price__gte=price_from, price__lte=price_to)
            print(products)

            context = {
                'products': products
            }
            return render(request, 'products/filtered_products.html', context=context)
