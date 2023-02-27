from django import template
from shop.models import *

register = template.Library()


@register.inclusion_tag('shop/list_category.html')
def show_category():
    category = Category.objects.all()
    return {"category": category}


@register.inclusion_tag('shop/footer.html')
def show_footer():
    contacts = Contacts.objects.all()
    return {"contacts": contacts}
