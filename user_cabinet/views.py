import zoneinfo
import datetime
from django.contrib.auth.hashers import check_password
from django.core.paginator import Paginator
from django.http import HttpResponse
from user_cabinet.forms import ChangeUserForm, ChangePasswordForm
from django.shortcuts import render, get_object_or_404
from orders.models import OrderItem, Order


def cabinet(request):
    return render(request, 'cabinet/cabinet.html')


def cart_profile(request):
    return render(request, 'cabinet/cart_profile.html')


def edit_profile(request):
    if request.method == 'POST':
        t = datetime.datetime.now()
        current_user = request.user
        user_data = request.POST
        form = ChangeUserForm(user_data, instance=current_user)
        user_data._mutable = True
        user_data['username'] = current_user
        user_data['is_active'] = 'on'
        user_data['date_joined'] = datetime.datetime(t.year, t.month, t.day, t.hour, t.minute, t.second,
                                                     tzinfo=zoneinfo.ZoneInfo(key='UTC'))
        user_data._mutable = False
        print(user_data)
        if form.is_valid():
            form.save()
            return render(request, 'cabinet/user_data_change_successful.html')
        else:
            return HttpResponse('Error')
    else:
        form = ChangeUserForm(instance=request.user)
        return render(request, 'cabinet/edit_profile.html', {'form': form})


def change_password(request):
    current_user = request.user
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            old_password = request.POST.get("old_password")
            if check_password(old_password, current_user.password):
                form.save()
                return render(request, 'cabinet/change_password_successful.html')
            else:
                return HttpResponse('Error')
    else:
        form = ChangePasswordForm(request.user)
    return render(request, 'cabinet/change_password.html', {'form': form, 'current_user': current_user})


def history_orders(request):
    orders = Order.objects.filter(email=request.user.email).values('id', 'created', 'paid')
    orders_item = OrderItem.objects.all()
    total_price = 0
    q_items = 0

    for i in orders:
        for o in orders_item:
            if i['id'] == o.order_id:
                total_price += o.price * o.quantity
                q_items += 1
        i.update({'total_price': total_price, 'q_items': q_items})
        q_items = 0
        total_price = 0

    paginator = Paginator(orders, 1)
    page_number = request.GET.get('page')
    pages = paginator.get_page(page_number)
    context = {'orders_item': orders_item, 'orders': orders, 'pages': pages}

    return render(request, 'cabinet/history_orders.html', context=context)


def detail_history_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    orders_item = OrderItem.objects.filter(order_id=order_id)
    for i in orders_item:
        i.__dict__.update({"total_price": i.price * i.quantity})

    context = {'order': order, 'orders_item': orders_item}
    return render(request, 'cabinet/detail_history_order.html', context)
