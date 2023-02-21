from django.urls import path, re_path, include
from . import views


urlpatterns = [
    re_path(r'^$', views.cart_detail, name='cart_detail'),
    re_path(r'^add/(?P<product_id>\d+)/$', views.cart_add, name='cart_add'),
    re_path(r'^remove-cabinet/(?P<product_id>\d+)/$', views.cart_remove_cabinet, name='cart_remove_cabinet'),
    re_path(r'^remove-cart/(?P<product_id>\d+)/$', views.cart_remove, name='cart_remove'),
]