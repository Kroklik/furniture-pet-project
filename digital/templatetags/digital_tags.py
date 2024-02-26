from digital.models import Category, FavoriteProduct, OrderProduct
from django import template

register = template.Library()


@register.simple_tag()
def get_categories():
    categories = Category.objects.filter(parent=None)
    return categories


@register.simple_tag()
def get_favorite_products(user):
    favorite_products = FavoriteProduct.objects.filter(user=user)
    products = [i.product for i in favorite_products]
    return products


@register.simple_tag()
def get_normal_price(price):
    return f'{int(price):_}'.replace('_', ' ')


