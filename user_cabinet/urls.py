from django.urls import path, re_path, include
from . import views
from .views import *

urlpatterns = [
    path('', views.cabinet, name='cabinet'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('change_password', views.change_password, name='change_password'),
    path('change_password/change_pass_successful', views.change_password, name='change_pass_successful'),
    path('cart_profile', views.cart_profile, name='cart_profile'),
    path('history_orders', views.history_orders, name='history_orders'),
    path('history_orders/<int:order_id>/', views.detail_history_order, name='detail_history_order'),
]
