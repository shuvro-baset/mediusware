from django.shortcuts import render
from django.views import generic
from django.views.generic import ListView, CreateView, UpdateView
from django.core.paginator import Paginator
from product.models import Variant, Product, ProductImage, ProductVariantPrice
from django.db.models import Q

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

# showing products and filter products
class ProductsView(generic.TemplateView):
    template_name = 'products/list.html'

    def get(self, request):
        # getting products data from ProductVariantPrice model
        products = ProductVariantPrice.objects.all()
        # todo: pagination start
        paginator = Paginator(products, 10)
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)
        # todo: pagination end
        context = {
            # 'products': products,
            "page_obj": page_obj
        }
        return render(request, self.template_name, context=context)

    # post method for filtering
    def post(self, request):
        if request.method == "POST":
            # getting filter data
            name = request.POST.get('title')
            price_from = request.POST.get('price_from')
            price_to = request.POST.get('price_to')
            product_ins = ProductVariantPrice.objects.all()
            # condition for not provided price
            if None or '' in [price_to, price_from]:
                products = product_ins.filter(product__title__icontains=name)
                paginator = Paginator(products, 10)
                page_number = request.GET.get("page", 1)
                page_obj = paginator.get_page(page_number)
                print("filter by name: ", page_obj)
                context = {
                    'page_obj': page_obj
                }
                return render(request, 'products/filtered_products.html', context=context)
            else:
                products = product_ins.filter(Q(product__title__icontains=name) | Q(price__gte=price_from) | Q(price__lte=price_to))

                paginator = Paginator(products, 10)
                page_number = request.GET.get("page", 1)
                page_obj = paginator.get_page(page_number)

                context = {
                    'page_obj': page_obj
                }
                return render(request, 'products/filtered_products.html', context=context)
