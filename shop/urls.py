from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('contacts/', contacts, name='contacts'),
    path('category/<slug:category_slug>/', ProductCategory.as_view(), name='category'),
    path('product_detail/<slug:product_slug>/', ShowProduct.as_view(), name='detail_product'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
]