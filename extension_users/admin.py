from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'address', 'city', 'phone_number', 'email_verify']


admin.site.register(User, UserAdmin)
