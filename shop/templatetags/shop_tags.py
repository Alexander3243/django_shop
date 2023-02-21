from django import template
from shop.models import *

register = template.Library()


@register.inclusion_tag('shop/list_category.html')
def show_category(sort=None, category_selected=0):
    if not sort:
        category = Category.objects.all()
    else:
        category = Category.objects.order_by(sort)

    return {"category": category, "category_selected": category_selected}


@register.inclusion_tag('shop/footer.html')
def show_footer():
    contacts = Contacts.objects.all()
    return {"contacts": contacts}
