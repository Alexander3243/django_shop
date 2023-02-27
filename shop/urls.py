from django.urls import path
from .views import *

urlpatterns = [

    path('', index, name='home'),
    path('contacts/', contacts, name='contacts'),
    path('category/<slug:category_slug>/', index, name='category'),
    path('product_detail/<slug:product_slug>/', product_detail, name='detail_product'),
    path('search/', index, name='search_results'),
]