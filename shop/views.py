from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseNotFound
from .models import *
from cart.forms import CartAddProductForm


def index(request, category_slug=None):
    if 'category' in request.path:
        slug = get_object_or_404(Category, slug=category_slug).slug
    else:
        slug = None

    search_query = request.GET.get('search', '')
    orderby = request.GET.get('orderby', '')
    min_price = request.GET.get('min_input')
    max_price = request.GET.get('max_input')
    products = filters(search_query=search_query, orderby=orderby, min_price=min_price, max_price=max_price, slug=slug)

    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    cart_product_form = CartAddProductForm()

    context = {'page_obj': page_obj,
               'cart_product_form': cart_product_form,
               }

    if min_price and max_price:
        context.update({'min_price': min_price,
                        'max_price': max_price,
                        'filter': '&min_input={}&max_input={}'.format(min_price, max_price)
                        })
    if orderby:
        context.update({'orderby': '&orderby={}'.format(orderby)})
    if search_query:
        context.update({'search': '&search={}'.format(search_query)})

    return render(request, 'shop/list_products.html', context=context)


def filters(search_query=None, orderby=None, min_price=None, max_price=None, slug=None):
    if min_price and max_price and orderby and slug:
        return Product.objects.filter(
            Q(category__slug=slug) & Q(price__gte=min_price) & Q(price__lte=max_price)).order_by(orderby)
    elif min_price and max_price and slug:
        return Product.objects.filter(
            Q(category__slug=slug) & Q(price__gte=min_price) & Q(price__lte=max_price))
    elif orderby and slug:
        return Product.objects.filter(category__slug=slug).order_by(orderby)
    elif slug:
        return Product.objects.filter(category__slug=slug)
    elif search_query:
        return Product.objects.filter(Q(name__iregex=search_query) | Q(price__icontains=search_query))
    elif min_price and max_price and orderby:
        return Product.objects.filter(Q(price__gte=min_price) & Q(price__lte=max_price)).order_by(orderby)
    elif min_price and max_price:
        return Product.objects.filter(Q(price__gte=min_price) & Q(price__lte=max_price))
    elif orderby:
        return Product.objects.all().order_by(orderby)
    else:
        return Product.objects.all()


def contacts(request):
    contact = Contacts.objects.all()
    context = {'contact': contact}
    return render(request, 'shop/contacts.html', context=context)


def pageNotFound(exception):
    return HttpResponseNotFound('<h1> Страница не найдена </h1>')


def product_detail(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    cart_product_form = CartAddProductForm()
    context = {'product': product, 'cart_product_form': cart_product_form}
    return render(request, 'shop/product_detail.html', context=context)
