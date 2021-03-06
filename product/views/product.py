from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic import ListView, CreateView, UpdateView
from django.core.paginator import Paginator
from product.models import Variant, Product, ProductImage, ProductVariantPrice, ProductVariant
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
        # getting variants
        variants = ProductVariant.objects.all()
        colors = []
        sizes = []
        styles = []
        for v in variants:
            if v.variant_id == 1:
                color = v.variant_title
                if color not in colors:
                    colors.append(color)
            if v.variant_id == 2:
                size = v.variant_title
                if size not in sizes:
                    sizes.append(size)
            if v.variant_id == 3:
                style = v.variant_title
                if style not in styles:
                    styles.append(style)
        print("variants: ", colors)
        # todo: pagination start
        paginator = Paginator(products, 10)
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)
        # todo: pagination end
        context = {
            # 'products': products,
            "page_obj": page_obj,
            "colors": colors,
            "sizes": sizes,
            "styles": styles,
        }
        return render(request, self.template_name, context=context)

    # post method for filtering
    def post(self, request):
        if request.method == "POST":
            # getting filter data
            name = request.POST.get('title')
            price_from = request.POST.get('price_from')
            price_to = request.POST.get('price_to')
            variant = request.POST.get('variant')
            product_ins = ProductVariantPrice.objects.all()
            # condition for not provided price
            if None or '' in [price_to, price_from, variant]:
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
                products = product_ins.filter(
                    Q(product__title__icontains=name) | Q(price__gte=price_from) | Q(price__lte=price_to))

                paginator = Paginator(products, 10)
                page_number = request.GET.get("page", 1)
                page_obj = paginator.get_page(page_number)

                context = {
                    'page_obj': page_obj
                }
                return render(request, 'products/filtered_products.html', context=context)


# show single product and update product data
class ProductsEditView(generic.TemplateView):
    template_name = 'products/single_product.html'

    def get(self, request, id):
        # getting product data
        product = ProductVariantPrice.objects.get(id=id)
        context = {
            "product": product
        }
        return render(request, 'products/single_product.html', context=context)

    def post(self, request, id):
        # receiving input value for update product info
        title = request.POST.get("title")
        desc = request.POST.get("desc")
        sku = request.POST.get("sku")
        color = request.POST.get("color")
        size = request.POST.get("size")
        style = request.POST.get("style")

        # getting product instance
        product_ins = Product.objects.filter(id=id).first()
        # update product title, description, sku
        product_ins.title = title
        product_ins.description = desc
        product_ins.sku = sku
        product_ins.save()

        # getting variant instance and update product color
        variant_ins_color = ProductVariant.objects.filter(product_id=id, variant_id=1).first()
        variant_ins_color.variant_title = color
        variant_ins_color.save()

        # getting variant instance and update product size
        variant_ins_size = ProductVariant.objects.filter(product_id=id, variant_id=2).first()
        variant_ins_size.variant_title = size
        variant_ins_size.save()

        # getting variant instance and update product style
        variant_ins_style = ProductVariant.objects.filter(product_id=id, variant_id=3).first()
        variant_ins_style.variant_title = style
        variant_ins_style.save()

        return redirect('/product/list')
