from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseNotFound
from .models import *
from django.views.generic import ListView, DetailView
from cart.forms import CartAddProductForm


class IndexView(ListView):
    model = Product
    paginate_by = 6
    template_name = 'shop/list_products.html'

    def get_queryset(self):
        orderby = self.request.GET.get("orderby", "")
        min_price = self.request.GET.get('min_input')
        max_price = self.request.GET.get('max_input')
        if min_price and max_price and orderby:
            return Product.objects.filter(Q(price__gte=min_price) & Q(price__lte=max_price)).order_by(orderby)
        elif min_price and max_price:
            return Product.objects.filter(Q(price__gte=min_price) & Q(price__lte=max_price))
        elif orderby:
            return Product.objects.all().order_by(orderby)
        return Product.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        min_price = self.request.GET.get('min_input')
        max_price = self.request.GET.get('max_input')
        orderby = self.request.GET.get('orderby', '')

        if min_price and max_price:
            context['min_price'] = min_price
            context['max_price'] = max_price
            context['filter'] = '&min_input={}&max_input={}'.format(min_price, max_price)
        if orderby:
            context['orderby'] = '&orderby={}'.format(orderby)
        context['cart_product_form'] = CartAddProductForm()
        return context


class ProductCategory(ListView):
    model = Product
    template_name = 'shop/list_products.html'
    paginate_by = 6

    def get_queryset(self):
        slug = self.kwargs['category_slug']
        orderby = self.request.GET.get('orderby', '')
        min_price = self.request.GET.get('min_input')
        max_price = self.request.GET.get('max_input')

        if min_price and max_price and orderby:
            return Product.objects.filter(
                Q(category__slug=slug) & Q(price__gte=min_price) & Q(price__lte=max_price)).order_by(orderby)
        elif min_price and max_price:
            return Product.objects.filter(
                Q(category__slug=slug) & Q(price__gte=min_price) & Q(price__lte=max_price))
        elif orderby:
            return Product.objects.filter(category__slug=slug).order_by(orderby)
        return Product.objects.filter(category__slug=slug)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        min_price = self.request.GET.get('min_input')
        max_price = self.request.GET.get('max_input')
        orderby = self.request.GET.get('orderby', '')
        context['category_selected'] = self.request.path
        context['cart_product_form'] = CartAddProductForm()

        if orderby:
            context['orderby'] = '&orderby={}'.format(orderby)

        if min_price and max_price:
            context['min_price'] = min_price
            context['max_price'] = max_price
            context['filter'] = '&min_input={}&max_input={}'.format(min_price, max_price)

        return context


class SearchResultsView(ListView):
    model = Product
    template_name = 'shop/list_products.html'
    paginate_by = 6

    def get_queryset(self):
        search_query = self.request.GET.get('search', '')
        return Product.objects.filter(Q(name__iregex=search_query) | Q(price__icontains=search_query))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        result = len(context['paginator'].__dict__['object_list'])
        search_query = self.request.GET.get('search', '')

        if search_query:
            context['search'] = '&search={}'.format(search_query)

        context['cart_product_form'] = CartAddProductForm()
        context['result'] = result
        print(1)
        return context


class ShowProduct(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    slug_url_kwarg = 'product_slug'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['cart_product_form'] = CartAddProductForm()
        return context


def contacts(request):
    contact = Contacts.objects.all()
    context = {'contact': contact}
    return render(request, 'shop/contacts.html', context=context)


def pageNotFound(exception):
    return HttpResponseNotFound('<h1> Страница не найдена </h1>')


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    context = {'product': product, 'cart_product_form': cart_product_form}
    return render(request, 'shop/product/detail.html', context=context)
