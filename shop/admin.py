from django.contrib import admin
from .models import Category, Product, Contacts


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'vendor_code', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'vendor_code', 'available']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Product, ProductAdmin)


class ContactsAdmin(admin.ModelAdmin):
    list_display = ['name', 'data', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Contacts, ContactsAdmin)
