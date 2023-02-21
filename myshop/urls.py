"""myshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('cart/', include(('cart.urls', 'cart'), namespace='cart')),

]

urlpatterns += [
    path('orders/', include(('orders.urls', 'orders'), namespace='orders')),
]

urlpatterns += [
    path('user_cabinet/', include(('user_cabinet.urls', 'user_cabinet'), namespace='user_cabinet')),
]

urlpatterns += [
    path('auth_and_reg/', include(('auth_and_reg.urls', 'auth_and_reg'), namespace='auth_and_reg')),
]

urlpatterns += [
    path('', include('shop.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
