from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register, name='register'),
    path('password_reset/done/', PasswordResetUserDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>', PasswordResetUserConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', PasswordResetUserCompleteView.as_view(), name='password_reset_complete'),
    path('password_reset/', PasswordResetUserView.as_view(), name='password_reset_form'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
]
