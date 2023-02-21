from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from django.http import QueryDict
from django.core.mail import EmailMessage


def order_create(request):
    cart = Cart(request)
    domain = get_current_site(request)

    if request.user.is_authenticated:
        if cart:
            user_data = QueryDict()
            user_data._mutable = True
            user_data.update({'first_name': request.user.first_name,
                              'last_name': request.user.last_name,
                              'email': request.user.email,
                              'address': request.user.address,
                              'city': request.user.city,
                              'phone_number': request.user.phone_number
                              })
            user_data._mutable = False
            form = OrderCreateForm(user_data)
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])

            cart.clear()
            send_order_email(order=order, cart=cart, domain=domain)

            return render(request, 'orders/order/created.html', {'order': order})
        return redirect('home')

    elif request.user.is_anonymous:
        if cart:
            form = OrderCreateForm(request.POST)
            if form.is_valid():
                order = form.save()
                for item in cart:
                    OrderItem.objects.create(order=order,
                                             product=item['product'],
                                             price=item['price'],
                                             quantity=item['quantity'])

                cart.clear()
                send_order_email(order=order, cart=cart, domain=domain)
                return render(request, 'orders/order/created.html', {'order': order})
            else:
                form = OrderCreateForm
            return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})
        return redirect('home')


def send_order_email(order, cart, domain):
    subject = '{}. Order №{}'.format(domain, order.pk)
    total = cart.get_total_price()
    message = render_to_string('orders/order/order_to_email.html', {'order': order, 'cart': cart, 'total': total})
    to_email = order.email
    email = EmailMessage(subject=subject, body=message, to=[to_email])
    email.content_subtype = 'html'
    email.send()
